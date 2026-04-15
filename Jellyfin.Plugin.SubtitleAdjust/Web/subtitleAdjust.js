/*
 * Jellyfin Subtitle Adjust - client-side stylesheet injector.
 *
 * This script is served by the Jellyfin.Plugin.SubtitleAdjust server plugin
 * at /SubtitleAdjust/ClientScript.js, with the placeholders (__FONT_SIZE__,
 * __BOTTOM_OFFSET__, etc.) replaced by the values saved in the plugin config.
 *
 * It injects a single <style> tag into the document that overrides the
 * subtitle-related CSS used by the Jellyfin web video player. The style tag
 * is re-inserted if it is removed (e.g. on navigation) so the overrides stay
 * active across views.
 */
(function () {
    'use strict';

    var config = {
        enabled: __ENABLED__,
        fontSizePercent: __FONT_SIZE__,
        bottomOffsetVh: __BOTTOM_OFFSET__,
        horizontalOffsetVw: __HORIZONTAL_OFFSET__,
        textColor: '__TEXT_COLOR__',
        backgroundColor: '__BACKGROUND_COLOR__',
        fontWeight: __FONT_WEIGHT__,
        textShadow: __TEXT_SHADOW__,
        fontFamily: '__FONT_FAMILY__'
    };

    var STYLE_ID = 'jellyfin-subtitle-adjust-style';

    function buildCss(cfg) {
        if (!cfg.enabled) {
            return '';
        }

        var scale = cfg.fontSizePercent / 100;
        var shadow = cfg.textShadow
            ? '1px 1px 2px rgba(0, 0, 0, 0.9), 0 0 3px rgba(0, 0, 0, 0.9)'
            : 'none';

        // Jellyfin web uses `.videoSubtitles` as the positioned container and
        // `.videoSubtitlesInner` as the inner text wrapper. We override both so
        // that scaling, color and positioning all take effect.
        return [
            '.videoSubtitles {',
            '    bottom: ' + cfg.bottomOffsetVh + 'vh !important;',
            '    transform: translateX(' + cfg.horizontalOffsetVw + 'vw) !important;',
            '    transition: bottom 0.15s ease, transform 0.15s ease;',
            '}',
            '.videoSubtitlesInner {',
            '    font-size: ' + (scale * 1.3) + 'em !important;',
            '    font-weight: ' + cfg.fontWeight + ' !important;',
            '    color: ' + cfg.textColor + ' !important;',
            '    background-color: ' + cfg.backgroundColor + ' !important;',
            '    text-shadow: ' + shadow + ' !important;',
            '    font-family: ' + cfg.fontFamily + ' !important;',
            '    line-height: 1.3 !important;',
            '    padding: 0.2em 0.5em !important;',
            '    border-radius: 4px;',
            '    display: inline-block;',
            '}',
            /* Some layouts wrap the inner element in additional spans. Make sure
             * that the computed font-size propagates to the actual text nodes. */
            '.videoSubtitlesInner * {',
            '    font-size: inherit !important;',
            '    color: inherit !important;',
            '}'
        ].join('\n');
    }

    function applyStyle() {
        var existing = document.getElementById(STYLE_ID);
        var css = buildCss(config);

        if (!existing) {
            existing = document.createElement('style');
            existing.id = STYLE_ID;
            existing.type = 'text/css';
            (document.head || document.documentElement).appendChild(existing);
        }

        if (existing.textContent !== css) {
            existing.textContent = css;
        }
    }

    function start() {
        applyStyle();

        // The Jellyfin web client is a SPA; nodes are swapped in and out of the
        // DOM frequently. Observe the document so we can re-insert our style
        // tag if a navigation removes it.
        if (window.MutationObserver) {
            var observer = new MutationObserver(function () {
                if (!document.getElementById(STYLE_ID)) {
                    applyStyle();
                }
            });
            observer.observe(document.documentElement, {
                childList: true,
                subtree: true
            });
        }

        // Expose a tiny API so power users can tweak live from the devtools.
        window.JellyfinSubtitleAdjust = {
            get config() {
                return Object.assign({}, config);
            },
            update: function (patch) {
                Object.assign(config, patch || {});
                applyStyle();
            },
            reapply: applyStyle
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start);
    } else {
        start();
    }
})();
