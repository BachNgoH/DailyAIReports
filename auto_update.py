import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutoCommitHandler(FileSystemEventHandler):
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def on_any_event(self, event):
        self.commit_changes()

    def commit_changes(self):
        # try:
            # Add changes to staging
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            
            # Commit changes
            commit_message = "Auto-commit: changes detected"
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            
            # Push changes
            subprocess.run(["git", "push"], cwd=self.repo_path, check=True)
            
            print(f"Changes committed and pushed with message: {commit_message}")
        # except subprocess.CalledProcessError as e:
        #     print(f"Error during Git operation: {e}")

def monitor_directory(repo_path):
    event_handler = GitAutoCommitHandler(repo_path)
    observer = Observer()
    observer.schedule(event_handler, path=repo_path, recursive=True)
    observer.start()
    print(f"Started monitoring {repo_path} for changes...")

    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    repo_path = "/media/gb2t/Data/DailyAIReports"  # Change this to your repository path
    monitor_directory(repo_path)
