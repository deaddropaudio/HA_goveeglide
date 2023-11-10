<h1 align='center'>Govee Glide for Home Assistant</h1>
<h4 align='center'>(a hacky single IP custom component to integrate Govee lights into HA via local API)</h3>


## Motivation / Scope

Look, I'm not a brilliant HA-modding wizard - I bought a Govee Glide (https://eu.govee.com/products/govee-glide-wall-light) because it's rad but couldn't find any integrations to make it work. <br/>
So, a weekend later I achieved my MVP: **app make light go bling (in technical terms)**

My main ressources were the HA API docs https://developers.home-assistant.io/docs/core/entity/light/ and the Govee Local API doc https://app-h5.govee.com/user-manual/wlan-guide

If you want to fix/ improve something - I'd be more than happy to accept pull requests. <3


## Functionality

- Adding a single Govee Light to Home Assistant as a light entity via static IP
- Controls: On/ Off, Color, Brightness


## Todos
- implement local discovery of devices and support for multiple devices via UDP multicast


## Usage
0. Enable the local API for your light in the Govee App (see Step 1 @ https://app-h5.govee.com/user-manual/wlan-guide)
1. Lookup your devices static IP in your router.
2. Copy content of folder "govee_glide" into your config/custom_components folder
3. Add new entity to configuration.yaml:
  ```yaml
  light:
    - platform: govee_glide
      ip_address: 'YOUR DEVICES IP ADDRESS'`
  ```
4. Restart Home Assistant and try it.
