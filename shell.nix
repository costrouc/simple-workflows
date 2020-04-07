let
  pkgs = import <nixpkgs> {};

  pythonPackages = pkgs.python3Packages;
in
pkgs.mkShell {
  buildInputs = with pythonPackages; [
    pythonPackages.pyyaml
  ];
}
