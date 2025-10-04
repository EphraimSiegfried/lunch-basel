{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs =
    {
      self,
      flake-utils,
      nixpkgs,
    }:
    flake-utils.lib.eachDefaultSystem (system: {
      packages = {
        lunchf = nixpkgs.legacyPackages.${system}.callPackage ./lunchf/package.nix { };
        lunchb = nixpkgs.legacyPackages.${system}.callPackage ./lunchb/package.nix { };
      };
    })
    // {
      nixosModules.default =
        {
          config,
          lib,
          pkgs,
          ...
        }:
        let
          lunchf = pkgs.callPackage ./lunchf/package.nix { };
          lunchb = pkgs.callPackage ./lunchb/package.nix { };
        in
        {
          options.services.lunch-basel = {
            enable = lib.mkEnableOption "lunch-basel";
            lunchbPort = lib.mkOption {
              type = lib.types.int;
              default = 8218;
            };
            lunchfPort = lib.mkOption {
              type = lib.types.int;
              default = 3000;
            };
          };

          config = lib.mkIf config.services.lunch-basel.enable {
            systemd.services.lunchb = {
              description = "Lunch-Basel Backend Service";
              wantedBy = [ "multi-user.target" ];
              environment.PORT = toString config.services.lunch-basel.lunchbPort;
              serviceConfig = {
                ExecStart = "${lunchb}/bin/lunchb";
                User = "lunch-basel";
                Restart = "always";
              };
            };
            systemd.services.lunchf = {
              description = "Lunch-Basel Frontend Service";
              wantedBy = [ "multi-user.target" ];
              environment = {
                API_BASE_URL = "http://localhost:${toString config.services.lunch-basel.lunchbPort}";
                PORT = toString config.services.lunch-basel.lunchfPort;
              };
              serviceConfig = {
                ExecStart = "${lunchf}/bin/lunchf";
                User = "lunch-basel";
                Restart = "always";
              };
            };
          };
        };
    };
}
