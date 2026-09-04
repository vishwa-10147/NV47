import subprocess
import csv
from io import StringIO

def list_processes(limit: int = 20) -> dict:
    """Lists running processes using standard Windows tasklist."""
    try:
        result = subprocess.run(
            ["tasklist", "/FO", "CSV"],
            capture_output=True,
            text=True,
            check=True
        )
        
        reader = csv.reader(StringIO(result.stdout))
        # Skip header
        next(reader, None)
        
        processes = []
        for row in reader:
            if len(row) >= 5:
                processes.append({
                    "name": row[0],
                    "pid": row[1],
                    "session_name": row[2],
                    "session_num": row[3],
                    "mem_usage": row[4]
                })
        
        return {
            "success": True,
            "processes": processes[:limit],
            "total_count": len(processes)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
