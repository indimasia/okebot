{
  description = "Discord Bot Application";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    mach-nix.url = "github:DavHau/mach-nix";
  };

  outputs = { self, nixpkgs, flake-utils, mach-nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        mach = mach-nix.lib.${system};
        
        # Build the python environment from requirements.txt
        # mach-nix automatically resolves dependencies from PyPI
        pythonApp = mach.mkPython {
          requirements = builtins.readFile ./requirements.txt;
        };
        
        # Create a derivation that includes the source and the python env
        app = pkgs.stdenv.mkDerivation {
          pname = "dbot";
          version = "0.1.0";
          
          src = ./.;
          
          buildInputs = [ pythonApp ];
          
          installPhase = ''
            mkdir -p $out/bin
            mkdir -p $out/share/dbot
            
            # Copy necessary files
            cp bot.py config.py $out/share/dbot/
            
            # Create wrapper script
            makeWrapper ${pythonApp}/bin/python $out/bin/dbot \
              --add-flags "$out/share/dbot/bot.py" \
              --run "cd $out/share/dbot"
          '';
          
          nativeBuildInputs = [ pkgs.makeWrapper ];
        };

      in
      {
        packages.default = app;
        
        devShells.default = pkgs.mkShell {
          buildInputs = [ pythonApp ];
          
          shellHook = ''
            echo "Environment loaded. Run 'python bot.py' to start."
          '';
        };
      }
    );
}
