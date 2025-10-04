{ pkgs, ... }:
{
  languages.typescript.enable = true;
  packages = [ pkgs.nodejs ];
  enterShell = "npm install";
  env.API_BASE_URL = "http://localhost:8218";
  scripts.start.exec = "npm run dev";
}
