{
  lib,
  pkgs,
  buildNpmPackage,
}:
buildNpmPackage rec {
  pname = "lunchf";
  version = "0.1.0";
  src = lib.cleanSource ./.;
  npmDepsHash = "sha256-BxqN1GCmnOvnJwUO3Ld+NPv22cfd/nrcbgYWaHuphTo=";
  installPhase = ''
    mkdir -p $out/
    cp -r .next/standalone $out/standalone
    cp -r .next/static $out/standalone/.next/static
    cp -r public $out/standalone/public
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
