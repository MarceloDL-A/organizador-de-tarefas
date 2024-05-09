    Organizador de Tarefas/
    ├── build/
    │   └── TaskOrganizer/
    ├── dist/
    │   └── TaskOrganizer/
    ├── models/
    │   └── task.py
    ├── ui/
    │   ├── app.py
    │   ├── notes.py
    │   └── task_list.py
    ├── utils/
    │   ├── logger.py
    │   └── tooltip.py
    ├── main.py
    ├── TaskOrganizer.spec
    ├── tasks.json
    └── task_history.txt





```bash
Remove-Item -Recurse -Force .\build, .\dist
pyinstaller TaskOrganizer.spec
```
