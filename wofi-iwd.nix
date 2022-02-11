{ pkgs, lib, ... }:
with pkgs ; stdenv.mkDerivation rec {
  pname = "wofi-iwd";
  version = "20220210";
  src = ./.;
  installPhase = ''
    install -vd $out/bin
    install -vm 755 wofi_iwd.sh $out/bin
    install -vm 755 rofi_iwd.sh $out/bin
  '';
  meta = with lib ; {
    description = "iwd interface using rofi/wofi";
    homepage = https://github.com/tylerjl/wofi-iwd;
    platforms = [ "x86_64-linux" ];
    mainProgram = "rofi_iwd.sh";
  };
  propagatedBuildInputs = [ (callPackage ./iwd-scan.nix {}) ];
}
