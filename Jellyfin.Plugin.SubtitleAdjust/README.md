# Jellyfin Subtitle Adjust

A Jellyfin server plugin that lets you adjust the **position** and **size**
(and a few extras: color, font weight, text shadow, font family) of subtitles
as they are rendered in the Jellyfin web client.

## Features

- Change subtitle **font size** as a percentage of the default
- Move subtitles **up/down** by a viewport-height offset
- Shift subtitles **left/right** by a viewport-width offset
- Configure **text color**, **background color**, **font weight** and **font family**
- Optional **text shadow** for better legibility on bright scenes
- Simple **admin configuration page** under *Dashboard → Plugins → Subtitle Adjust*
- Changes apply **live** to the running web client (after reload)

## How it works

The plugin is a standard Jellyfin server plugin (`.dll`) with one extra
endpoint: `GET /SubtitleAdjust/ClientScript.js`. That endpoint returns a small
JavaScript file with the currently saved configuration baked in.

When the script runs in the Jellyfin web client it injects a `<style>` tag that
overrides the CSS used for the subtitle container (`.videoSubtitles`) and the
inner text element (`.videoSubtitlesInner`). The script re-installs the style
tag if the SPA removes it on navigation, so the overrides persist.

## Installation

### Option 1 — Add as a plugin repository (recommended)

1. In Jellyfin, go to **Dashboard → Plugins → Repositories → New Repository**.
2. **Repository URL**:
   ```
   https://raw.githubusercontent.com/RobinNotHood/idleGame/main/manifest.json
   ```
3. **Dashboard → Plugins → Catalog**, install **Subtitle Adjust**, restart Jellyfin.
4. Open **Dashboard → Plugins → Subtitle Adjust** and adjust the values to
   taste, then click **Save**.

### Option 2 — Manual install

1. Build the plugin:
   ```bash
   dotnet publish -c Release Jellyfin.Plugin.SubtitleAdjust/Jellyfin.Plugin.SubtitleAdjust.csproj
   ```
2. Copy `Jellyfin.Plugin.SubtitleAdjust.dll` and `meta.json` into your
   Jellyfin server's `plugins/SubtitleAdjust_1.0.0.0/` directory.
3. Restart Jellyfin.
4. Open the Jellyfin dashboard → **Plugins** → **Subtitle Adjust** and adjust
   the values to taste, then click **Save**.

## Loading the client script

Jellyfin server plugins cannot, on their own, inject scripts into the web
client. You have two options:

### Option A — Patch `index.html` (most reliable)

Add the following line just before `</body>` in
`jellyfin-web/index.html` on your server:

```html
<script src="/SubtitleAdjust/ClientScript.js" defer></script>
```

### Option B — Use a "Custom CSS/JS" plugin

If you already use a plugin that lets you inject JavaScript into the web
client (for example *Custom JavaScript* or a custom-branding plugin), point
it at `/SubtitleAdjust/ClientScript.js`.

## Runtime API

For debugging from the browser devtools:

```js
JellyfinSubtitleAdjust.config          // current config
JellyfinSubtitleAdjust.update({        // temporarily tweak settings
    fontSizePercent: 140,
    bottomOffsetVh: 18
});
JellyfinSubtitleAdjust.reapply();      // force-reapply the style tag
```

Changes made via `update()` only live until the next page load; persistent
changes should be made in the dashboard config page.

## Settings reference

| Setting              | Type     | Default                | Notes                                                   |
|----------------------|----------|------------------------|---------------------------------------------------------|
| `Enabled`            | bool     | `true`                 | Master switch                                           |
| `FontSizePercent`    | int      | `100`                  | Percentage of default subtitle size (25 – 400)          |
| `BottomOffsetVh`     | int      | `10`                   | Distance from bottom of video in vh units (0 – 90)      |
| `HorizontalOffsetVw` | int      | `0`                    | Horizontal shift in vw units (-50 – 50)                 |
| `FontWeight`         | int      | `400`                  | CSS font-weight (100 – 900)                             |
| `TextColor`          | string   | `#FFFFFF`              | Any CSS color                                           |
| `BackgroundColor`    | string   | `rgba(0, 0, 0, 0.5)`   | Any CSS color; use `transparent` to disable            |
| `FontFamily`         | string   | `inherit`              | CSS font-family stack                                   |
| `TextShadow`         | bool     | `true`                 | Adds a dark drop-shadow behind each character           |

## License

MIT
