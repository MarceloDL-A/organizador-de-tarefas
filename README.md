    ORGANIZADOR_DE_TAREFAS/
    ├── main.py
    ├── models/
    │   └── task.py
    ├── ui/
    │   └── app.py
    └── utils/
        ├── logger.py
        └── tooltip.py



```bash
Remove-Item -Recurse -Force .\build, .\dist
pyinstaller TaskOrganizer.spec
```
