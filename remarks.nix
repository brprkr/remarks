with import <nixpkgs> {};
pkgs.mkShell {
  NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [ pkgs.stdenv.cc.cc zlib ];
  NIX_LD = lib.fileContents "${stdenv.cc}/nix-support/dynamic-linker";

  buildInputs = [
    pkgs.python310
    pkgs.poetry
    pkgs.zlib
    pkgs.gnumake
  ];

  shellHooks = ''
    export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
    source ./venv/bin/activate
  '';
  
}
