using MediaBrowser.Model.Plugins;

namespace Jellyfin.Plugin.SubtitleAdjust.Configuration;

/// <summary>
/// Persisted plugin configuration containing the user's subtitle style preferences.
/// </summary>
public class PluginConfiguration : BasePluginConfiguration
{
    /// <summary>
    /// Initializes a new instance of the <see cref="PluginConfiguration"/> class
    /// with sensible defaults that match Jellyfin's native subtitle appearance.
    /// </summary>
    public PluginConfiguration()
    {
        Enabled = true;
        FontSizePercent = 100;
        BottomOffsetVh = 10;
        HorizontalOffsetVw = 0;
        TextColor = "#FFFFFF";
        BackgroundColor = "rgba(0, 0, 0, 0.5)";
        FontWeight = 400;
        TextShadow = true;
        FontFamily = "inherit";
    }

    /// <summary>
    /// Gets or sets a value indicating whether the subtitle adjustments are applied.
    /// </summary>
    public bool Enabled { get; set; }

    /// <summary>
    /// Gets or sets the font size, expressed as a percentage of the default
    /// subtitle size (100 = unchanged, 150 = 1.5x larger, 75 = smaller).
    /// </summary>
    public int FontSizePercent { get; set; }

    /// <summary>
    /// Gets or sets how far above the bottom of the video the subtitles
    /// should be rendered, in viewport-height units (vh). Higher moves subtitles up.
    /// </summary>
    public int BottomOffsetVh { get; set; }

    /// <summary>
    /// Gets or sets the horizontal offset from center, in viewport-width units (vw).
    /// Negative values move subtitles left, positive move them right.
    /// </summary>
    public int HorizontalOffsetVw { get; set; }

    /// <summary>
    /// Gets or sets the subtitle text color (CSS color string, e.g. "#FFFFFF").
    /// </summary>
    public string TextColor { get; set; }

    /// <summary>
    /// Gets or sets the subtitle background color (CSS color string,
    /// typically an rgba value with transparency).
    /// </summary>
    public string BackgroundColor { get; set; }

    /// <summary>
    /// Gets or sets the font weight (100-900). 400 = normal, 700 = bold.
    /// </summary>
    public int FontWeight { get; set; }

    /// <summary>
    /// Gets or sets a value indicating whether a text shadow should be rendered
    /// behind each subtitle character for improved legibility.
    /// </summary>
    public bool TextShadow { get; set; }

    /// <summary>
    /// Gets or sets the CSS font-family used to render subtitles.
    /// Use "inherit" to keep the Jellyfin default.
    /// </summary>
    public string FontFamily { get; set; }
}
