import tempfile
import os
import json
from pathlib import Path
from app.core.logger import EventLogger
from app.core.events import Event

def test_logger_initialization():
    with tempfile.TemporaryDirectory() as temp_dir:
        logger = EventLogger(log_dir=temp_dir)
        assert Path(temp_dir).exists()
        assert logger.log_file.name == "events.jsonl"

def test_logger_writes_event():
    with tempfile.TemporaryDirectory() as temp_dir:
        logger = EventLogger(log_dir=temp_dir)
        
        event = Event(event_type="TEST_EVENT", message="This is a test", data={"key": "value"})
        logger.log(event)
        
        assert logger.log_file.exists()
        
        with open(logger.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 1
            log_data = json.loads(lines[0])
            
            assert log_data["event_type"] == "TEST_EVENT"
            assert log_data["message"] == "This is a test"
            assert log_data["data"]["key"] == "value"
            assert "timestamp" in log_data

def test_logger_read_logs():
    with tempfile.TemporaryDirectory() as temp_dir:
        logger = EventLogger(log_dir=temp_dir)
        
        logger.log(Event(event_type="TEST_1", message="Message 1"))
        logger.log(Event(event_type="TEST_2", message="Message 2"))
        
        logs = logger.read_logs(limit=1)
        assert len(logs) == 1
        assert "TEST_2" in logs[0]
        
        logs_all = logger.read_logs(limit=10)
        assert len(logs_all) == 2
