with import <nixpkgs> {};
let
  shellHook = pkgs.writeShellApplication {
    name = "shellhook";
    text = ''
      export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH

      if ! [[ -d .venv ]]; then
        poetry env use python3.10
        poetry install
      else
        # shellcheck disable=SC1091
        source ./.venv/bin/activate
      fi
    '';
  };
in
pkgs.mkShell {
  NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [ pkgs.stdenv.cc.cc zlib ];
  NIX_LD = lib.fileContents "${stdenv.cc}/nix-support/dynamic-linker";

  buildInputs = [
    pkgs.python310
    pkgs.poetry
    pkgs.zlib
    pkgs.gnumake
  ];

  shellHooks = "${shellHook}/bin/shellhook";
  
}
