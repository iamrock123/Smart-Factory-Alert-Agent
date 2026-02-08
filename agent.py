from anomaly_detector import AnomalyDetector
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.status import Status

class AnomalyAlertAgent:
    def __init__(self, model_name="Qwen3:4b"):
        self.console = Console()
        self.detector = AnomalyDetector(data_path='data/test_data.csv')
        self.model_name = model_name
        self.knowledge_base = self._load_knowledge_base() # Load KB on init
        
        try:
            self.llm = ChatOllama(model=model_name)
        except Exception as e:
            self.console.print(f"[bold red]Error initializing Ollama:[/bold red] {e}")
            self.llm = None

    def _load_knowledge_base(self):
        """Loads the Knowledge Base content from markdown file."""
        try:
            with open("config/knowledge_base.md", "r") as f:
                return f.read()
        except FileNotFoundError:
            self.console.print("[yellow]Warning: config/knowledge_base.md not found. AI will run without grounding.[/yellow]")
            return "No Standard Operating Procedure available."

    def run(self):
        # Use Rich Status spinner to show loading animation
        with self.console.status("[bold green]Loading data and analyzing patterns...", spinner="dots"):
            self.detector.load_data()
            anomalies = self.detector.detect_anomalies()
        
        self.console.print(f"\n[bold cyan]Process Complete.[/bold cyan] Detected [bold red]{len(anomalies)}[/bold red] anomalies.\n")
        
        if not anomalies:
            self.console.print("[green]System Normal. No anomalies detected.[/green]")
            return

        # --- 1. Show Summary Table First ---
        self._print_summary_table(anomalies)

        # --- 2. Consolidated AI Reporting ---
        self.console.print("\n[bold white on blue] --- Generating Holistic System Diagnosis --- [/bold white on blue]\n")
        self.generate_consolidated_report(anomalies)
            
    def _print_summary_table(self, anomalies):
        """Prints the anomaly summary table."""
        table = Table(title="⚠️ Anomaly Detection Summary", show_header=True, header_style="bold magenta")
        table.add_column("Timestamp", style="cyan", no_wrap=True)
        table.add_column("Issue Detected") 
        table.add_column("Risk Score", justify="right")

        for anomaly in anomalies:
            # Colorize reasons
            formatted_reasons = []
            for r in anomaly['reasons']:
                if "CRITICAL" in r:
                    formatted_reasons.append(f"[bold red]{r}[/bold red]")
                elif "WARNING" in r:
                    formatted_reasons.append(f"[yellow]{r}[/yellow]")
                else:
                    formatted_reasons.append(r)

            # Style score
            score_style = "red" if anomaly['score'] > 10 else "yellow"
            table.add_row(
                str(anomaly['timestamp']),
                ", ".join(formatted_reasons),
                f"[{score_style}]{anomaly['score']:.2f}[/{score_style}]"
            )
        self.console.print(table)

    def generate_consolidated_report(self, anomalies):
        """
        Generates a SINGLE report analyzing the trend and overall health.
        """
        
        # Prepare aggregated data string
        anomaly_summary_text = ""
        for a in anomalies:
            anomaly_summary_text += f"- [{a['timestamp']}] Score: {a['score']} | Issues: {', '.join(a['reasons'])}\n"

        prompt_text = f"""
        You are a Senior Reliability Engineer.
        Review the anomaly timeline and provide a **Professional & Concise** System Diagnosis.
        
        [System Knowledge Base]:
        {self.knowledge_base}
        
        [Anomaly Timeline]:
        {anomaly_summary_text}
        
        **Output Requirements:**
        - Keep descriptions **brief and professional** (avoid wordy explanations).
        - Use bullet points for readability.
        
        **Output Format:**

        ### 1. Trend Analysis
        * **Evolution:** [1-2 sentences describing how the fault progressed over time]
        * **Primary Symptom:** [State the dominant issue identified]

        ### 2. Root Cause Hypothesis
        * **Diagnosis:** [The SINGLE most likely physical defect based on the KB]
        * **Evidence:**
          * [Timestamp]: [Brief specific observation]
          * [Timestamp]: [Brief specific observation]

        ### 3. Consolidated Action Plan
        1. [Action Step] - [Brief Reason]
        2. [Action Step] - [Brief Reason]
        """
        
        if self.llm:
            try:
                with self.console.status("[bold yellow]Synthesizing Holistic Report...", spinner="earth"):
                    response = self.llm.invoke(prompt_text)
                
                md = Markdown(response.content)
                self.console.print(Panel(md, title="🤖 AI Reliability Engineer: Holistic Diagnosis", border_style="green", expand=False))
                
            except Exception as e:
                self.console.print(f"[bold red][Error][/bold red] AI analysis failed: {e}")
        else:
             self.console.print("[dim]LLM client not initialized, skipping analysis.[/dim]")
        
        self.console.print("\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Anomaly Alert AI Agent")
    parser.add_argument("--model", type=str, default="Qwen3:4b", help="Ollama model name (default: Qwen3:4b)")
    args = parser.parse_args()
        
    agent = AnomalyAlertAgent(model_name=args.model)
    agent.run()
