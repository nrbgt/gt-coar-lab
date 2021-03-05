:: Copyright (c) 2021 University System of Georgia and GTCOARLab Contributors
:: Distributed under the terms of the BSD-3-Clause License
::
:: GTCOARLab-GPU 2021.03-0 defaults
::
@ECHO ON

SET PY_SCRIPT=                                                                                                                          ^
    import os, json, pathlib.Path as P;                                                                                                 ^
    S = P(os.environ['PREFIX']) / 'share/jupyter/lab/user-settings';                                                                    ^
    theme = S / '@jupyterlab/apputils-extension/themes.jupyterlab-settings'                                                             ^
    theme.parent.mkdir(parents=True, exist_ok=True)                                                                                     ^
    theme.write_text(json.dumps({'theme': 'GT COAR Light', 'theme-scrollbars': True}))                                                  ^
    term = S / '@jupyterlab/terminal-extension/themes.jupyterlab-settings'                                                              ^
    term.parent.mkdir(parents=True, exist_ok=True)                                                                                      ^
    term.write_text(json.dumps({'fontFamily': '\'Roboto Mono\', Menlo, Consolas, \'DejaVu Sans Mono\', monospace', 'fontSize': 14}))    ^

call %PREFIX%\python.exe -c %PY_SCRIPT%  || ECHO 'whatever, we tried'