    ORGANIZADOR_DE_TAREFAS/
    ├── main.py
    ├── models/
    │   └── task.py
    ├── ui/
    │   ├── app.py
    │   ├── task_list.py
    │   └── notes.py
    └── utils/
        ├── logger.py
        └── tooltip.py




```bash
Remove-Item -Recurse -Force .\build, .\dist
pyinstaller TaskOrganizer.spec
```
