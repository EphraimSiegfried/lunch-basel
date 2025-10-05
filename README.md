# Lunch Basel

Website which displays the daily menu of all the canteens/restaurants I like.

## Docker Deployment

Deploy with `docker compose up -d`. You can access the website locally at
http://localhost:3000.

## Nix Deployment

1. Add lunch-basel to your inputs:

   ```nix
   inputs = {
       ...
       lunch-basel.url =  "github:EphraimSiegfried/lunch-basel";
       ...
   }
   ```
2. Then add it to the nixosConfiguration modules:

   ```nix
   modules = [
       ...
       inputs.lunch-basel.nixosModules.default
       ...
   ]
   ```

3. Finally enable the service:

   ```nix
   { config, ... }:
   let
     port = 3991;
   in
   {
     services.lunch-basel = {
       enable = true;
       lunchfPort = port;
     };
     # Optionally expose service with nginx
     services.nginx.virtualHosts."your-domain" = {
       locations."/" = {
         proxyPass = "http://127.0.0.1:${toString port}";
       };
     };
   }
   ```

## Modifications

To add a restaurant you only have to write a class which inherits from the
Restaurant class and write all it's methods
[here](./backend/lunchb/restaurants.py).
