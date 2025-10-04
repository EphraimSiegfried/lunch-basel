{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs =
    {
      self,
      flake-utils,
      nixpkgs,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        packages = {
          lunchf = pkgs.callPackage ./lunchf/package.nix { };
          lunchb = pkgs.callPackage ./lunchb/package.nix { };
        };
      }
    )
    // {
      nixosModules = {
        default = import ./lunch-basel.nix;

      };
    };
}
