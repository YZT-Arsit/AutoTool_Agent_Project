import os
import pytest
from autotoolbench.tools.file_tool import FileTool, FileWriteTool
from autotoolbench.tools.sqlite_tool import SQLiteTool
from autotoolbench.tools.python_tool import PythonExecTool
# run_tests_tool not used in tests directly

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

def setup_module(module):
    # ensure data present
    import scripts.make_data as md
    md.main()


def test_file_read_write(tmp_path, monkeypatch):
    # write using tool
    ftw = FileWriteTool()
    res = ftw.run({"path":"test.txt","content":"hello"})
    assert res.ok
    # read back
    ftr = FileTool()
    res2 = ftr.run({"path":"test.txt"})
    assert res2.ok and "hello" in res2.output
    # path escape
    res3 = ftr.run({"path":"../etc/passwd"})
    assert not res3.ok

def test_sqlite_read():
    st = SQLiteTool()
    res = st.run({"query":"SELECT name from users"})
    assert res.ok
    assert isinstance(res.output, list)

def test_python_exec():
    pt = PythonExecTool()
    res = pt.run({"code":"a=1+2"})
    assert res.ok
    assert res.output.get("a") == 3
    # try forbidden import
    r2 = pt.run({"code":"import os"})
    assert not r2.ok
