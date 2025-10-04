{
  lib,
  pkgs,
  buildNpmPackage,
}:
buildNpmPackage rec {
  pname = "lunchf";
  version = "0.1.0";
  src = lib.cleanSource ./.;
  npmDepsHash = "sha256-5pYKBj41nkqlnUmjS50m83ln4f/S6j0+npV5zeRUJnk=";
  installPhase = ''
    mkdir -p $out/
    cp -r .next/standalone $out/standalone
    mkdir -p $out/bin
    local node_exec="${lib.getExe pkgs.nodejs}"
    local server_script="$out/standalone/server.js"
    cat > $out/bin/${pname} << EOF
    #!/bin/sh
    exec $node_exec $server_script "\$@"
    EOF

    chmod +x $out/bin/${pname}
  '';

}
