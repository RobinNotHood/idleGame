# Jellyfin Subtitle Adjust

A Jellyfin server plugin that lets you adjust **subtitle position and size**
(plus color, weight, background, font, and text shadow) in the Jellyfin web
client.

The plugin itself lives in [`Jellyfin.Plugin.SubtitleAdjust/`](./Jellyfin.Plugin.SubtitleAdjust/).
See that directory's [README](./Jellyfin.Plugin.SubtitleAdjust/README.md) for
installation, configuration, and usage instructions.

## Quick build

```bash
dotnet publish -c Release \
    Jellyfin.Plugin.SubtitleAdjust/Jellyfin.Plugin.SubtitleAdjust.csproj
```

Copy the resulting `Jellyfin.Plugin.SubtitleAdjust.dll` into your Jellyfin
server's `plugins/SubtitleAdjust_1.0.0.0/` directory and restart Jellyfin.
