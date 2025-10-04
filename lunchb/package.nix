{ lib, pkgs }:
let
  python = pkgs.python313Packages;
in
python.buildPythonPackage {
  name = "lunchb";
  version = "0.1.0";
  src = lib.cleanSource ./.;
  pyproject = true;
  dependencies = with python; [
    beautifulsoup4
    flask
    gunicorn
    pypdf
    requests
  ];

  build-system = [
    python.uv-build
  ];
}
