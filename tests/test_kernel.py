from app.core.kernel import NV001Kernel
from app.core.tasks import Task
from app.core.events import Event

def test_kernel_initialization():
    kernel = NV001Kernel()
    assert not kernel.running
    assert len(kernel.tasks) == 0
    assert kernel.tools is not None
    assert kernel.permissions is not None

def test_kernel_start_stop():
    kernel = NV001Kernel()
    
    kernel.start()
    assert kernel.running
    
    kernel.stop()
    assert not kernel.running

def test_kernel_create_task():
    kernel = NV001Kernel()
    task = kernel.create_task("system info")
    
    assert isinstance(task, Task)
    assert task.command == "system info"
    assert len(kernel.tasks) == 1
    assert kernel.tasks[0] == task

def test_kernel_execute_task():
    kernel = NV001Kernel()
    task = kernel.create_task("system info")
    
    kernel.execute_task(task)
    
    assert task.status in ["completed", "failed"]

def test_kernel_task_dependencies():
    kernel = NV001Kernel()
    dep_task = kernel.create_task("system info")
    dep_task.status = "running"
    
    task = kernel.create_task("system info")
    task.dependencies.append(dep_task.task_id)
    
    kernel.execute_task(task)
    assert task.status == "created" # Deferred
    
    dep_task.status = "completed"
    kernel.execute_task(task)
    assert task.status in ["completed", "failed"]

def test_kernel_task_retries():
    kernel = NV001Kernel()
    task = kernel.create_task("invalid_command")
    task.max_retries = 1
    
    kernel.execute_task(task)
    
    # Task should fail, retry once, fail again
    assert task.status == "failed"
    assert task.retries == 1
