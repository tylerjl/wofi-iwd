{
  description = "iwd interface using rofi/wofi";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, flake-utils, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        packages.wofi-iwd = pkgs.callPackage ./wofi-iwd.nix {};
        packages.iwd-scan = pkgs.callPackage ./iwd-scan.nix {};
        defaultPackage = self.packages.${system}.wofi-iwd;
      }
    ) // {
      overlay = final: prev: {
        iwd-scan = prev.callPackage ./iwd-scan.nix {};
        wofi-iwd = prev.callPackage ./wofi-iwd.nix {};
      };
    };
}
