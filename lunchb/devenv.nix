{
  languages.python = {
    enable = true;
    uv = {
      enable = true;
      sync.enable = true;
    };
  };
  scripts.start.exec = "uv run lunchb";
  enterShell = ''
    . .devenv/state/venv/bin/activate
  '';
}
