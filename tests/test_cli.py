import pytest
from app.core.kernel import NV001Kernel

def test_kernel_cli_flow():
    kernel = NV001Kernel()
    kernel.start()
    
    # Test a basic deterministic flow
    task = kernel.create_task("system info")
    kernel.execute_task(task)
    
    assert task.status == "completed"
    assert task.result["success"] is True
    
    # Test background daemon scheduler
    kernel.daemon.add_task(interval_seconds=1, command="list processes")
    assert len(kernel.daemon.tasks) == 1
    
    kernel.stop()
