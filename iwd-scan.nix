{ pkgs, ... }: with pkgs ;
writers.writePython3Bin "iwd-scan" {
  libraries = with python3Packages; [ dbus-python ];
} (builtins.readFile ./iwd-scan.py)
