{
  lib,
  config,
  ...
}:
with lib;
let
  name = "lunch-basel";
  cfg = config.services.${name};
  lunchf = pkgs.callPackage ./lunchf/package.nix { };
  lunchb = pkgs.callPackage ./lunchb/package.nix { };
in
{
  options.services.hello = {
    enable = mkEnableOption "${name}";
    lunchbPort = mkOption {
      type = types.int;
      default = 8218;
    };
    lunchfPort = mkOption {
      type = types.int;
      default = 3000;
    };
  };

  config = mkIf cfg.enable {
    systemd.services.lunchb = {
      description = "Lunch-Basel Backend Service";
      wantedBy = [ "multi-user.target" ];
      environment = {
        PORT = "${cfg.lunchbPort}";
      };
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
        API_BASE_URL = "http://localhost:8218";
        PORT = "${cfg.lunchfPort}";
      };
      serviceConfig = {
        ExecStart = "${lunchf}/bin/lunchf";
        User = "lunch-basel";
        Restart = "always";
      };
    };
  };
}
