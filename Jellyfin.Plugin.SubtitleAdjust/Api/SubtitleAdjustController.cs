using System.IO;
using System.Reflection;
using Jellyfin.Plugin.SubtitleAdjust.Configuration;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace Jellyfin.Plugin.SubtitleAdjust.Api;

/// <summary>
/// Serves the client-side script used to apply subtitle styling in the Jellyfin web client.
/// </summary>
/// <remarks>
/// The endpoint is anonymous so that it can be loaded from the web client's login page
/// or before a user session is established. It only returns CSS/JS derived from the
/// current plugin configuration and contains no sensitive data.
/// </remarks>
[ApiController]
[Route("SubtitleAdjust")]
[AllowAnonymous]
public class SubtitleAdjustController : ControllerBase
{
    /// <summary>
    /// Returns a JavaScript file that applies the configured subtitle style overrides.
    /// Users (or admins) should load this script from their Jellyfin web client by
    /// either adding it to <c>index.html</c> or through a client customization plugin.
    /// </summary>
    /// <returns>A JavaScript file with the active configuration baked in.</returns>
    [HttpGet("ClientScript.js")]
    [Produces("application/javascript")]
    public ActionResult GetClientScript()
    {
        PluginConfiguration config =
            Plugin.Instance?.Configuration ?? new PluginConfiguration();

        Assembly assembly = typeof(SubtitleAdjustController).Assembly;
        const string ResourceName = "Jellyfin.Plugin.SubtitleAdjust.Web.subtitleAdjust.js";

        using Stream? stream = assembly.GetManifestResourceStream(ResourceName);
        if (stream is null)
        {
            return NotFound();
        }

        using var reader = new StreamReader(stream);
        string template = reader.ReadToEnd();

        string js = template
            .Replace("__ENABLED__", config.Enabled ? "true" : "false")
            .Replace("__FONT_SIZE__", config.FontSizePercent.ToString(System.Globalization.CultureInfo.InvariantCulture))
            .Replace("__BOTTOM_OFFSET__", config.BottomOffsetVh.ToString(System.Globalization.CultureInfo.InvariantCulture))
            .Replace("__HORIZONTAL_OFFSET__", config.HorizontalOffsetVw.ToString(System.Globalization.CultureInfo.InvariantCulture))
            .Replace("__TEXT_COLOR__", EscapeForJs(config.TextColor))
            .Replace("__BACKGROUND_COLOR__", EscapeForJs(config.BackgroundColor))
            .Replace("__FONT_WEIGHT__", config.FontWeight.ToString(System.Globalization.CultureInfo.InvariantCulture))
            .Replace("__TEXT_SHADOW__", config.TextShadow ? "true" : "false")
            .Replace("__FONT_FAMILY__", EscapeForJs(config.FontFamily));

        return Content(js, "application/javascript");
    }

    private static string EscapeForJs(string? value)
    {
        if (string.IsNullOrEmpty(value))
        {
            return string.Empty;
        }

        return value
            .Replace("\\", "\\\\")
            .Replace("'", "\\'")
            .Replace("\"", "\\\"")
            .Replace("\r", string.Empty)
            .Replace("\n", string.Empty);
    }
}
