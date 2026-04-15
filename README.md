# Jellyfin Subtitle Adjust

A Jellyfin server plugin that lets you adjust **subtitle position and size**
(plus color, weight, background, font, and text shadow) in the Jellyfin web
client.

## Install (recommended — as a plugin repository)

1. In Jellyfin, go to **Dashboard → Plugins → Repositories → New Repository**.
2. Fill in the form:
    - **Repository Name**: `Subtitle Adjust`
    - **Repository URL**:
      ```
      https://raw.githubusercontent.com/RobinNotHood/idleGame/main/manifest.json
      ```
3. Click **Add**.
4. Go to **Dashboard → Plugins → Catalog**, find **Subtitle Adjust**, and click **Install**.
5. Restart Jellyfin when prompted.
6. Open **Dashboard → Plugins → Subtitle Adjust** and tweak the settings.

## Install (manual)

1. Download the latest `subtitle-adjust-<version>.zip` from the
   [Releases](https://github.com/RobinNotHood/idleGame/releases) page.
2. Extract it into
   `<jellyfin-data>/plugins/SubtitleAdjust_<version>/` so the folder contains
   `Jellyfin.Plugin.SubtitleAdjust.dll` and `meta.json`.
3. Restart Jellyfin.

## Load the client-side script

Jellyfin server plugins cannot inject JS into the web client on their own.
After installing, enable the overrides by loading the plugin's client script
in `jellyfin-web/index.html` (on your server) — add this line just before
`</body>`:

```html
<script src="/SubtitleAdjust/ClientScript.js" defer></script>
```

Alternatively, use any "custom JS" plugin and point it at
`/SubtitleAdjust/ClientScript.js`.

## Settings

All configurable from the plugin's dashboard page:

| Setting              | Default                | Notes                                                   |
|----------------------|------------------------|---------------------------------------------------------|
| Enabled              | `true`                 | Master switch                                           |
| Font size (%)        | `100`                  | 25 – 400 (100 = Jellyfin default)                       |
| Bottom offset (vh)   | `10`                   | Higher = subtitles pushed further up                    |
| Horizontal offset (vw) | `0`                  | Negative = left, positive = right                       |
| Font weight          | `400`                  | 100 – 900                                               |
| Text color           | `#FFFFFF`              | Any CSS color                                           |
| Background color     | `rgba(0, 0, 0, 0.5)`   | Use `transparent` to disable                            |
| Font family          | `inherit`              | CSS font-family stack                                   |
| Text shadow          | `true`                 | Dark drop-shadow behind each character                  |

## Build from source

```bash
dotnet publish -c Release \
    Jellyfin.Plugin.SubtitleAdjust/Jellyfin.Plugin.SubtitleAdjust.csproj
```

The built DLL lands in `Jellyfin.Plugin.SubtitleAdjust/bin/Release/net8.0/`.
See [`Jellyfin.Plugin.SubtitleAdjust/README.md`](./Jellyfin.Plugin.SubtitleAdjust/README.md)
for the full architecture and runtime API.

## Releasing

Pushing a tag of the form `v1.2.3.4` triggers the
[`release`](./.github/workflows/release.yml) workflow, which:

- Builds the plugin
- Zips `Jellyfin.Plugin.SubtitleAdjust.dll` + `meta.json`
- Publishes a GitHub Release with the zip attached
- Regenerates `manifest.json` with the real download URL, MD5 checksum and
  timestamp, then commits it back to the default branch

Once a release exists on the default branch, any Jellyfin server that added
the repository URL above will see the new version in its plugin catalog.
