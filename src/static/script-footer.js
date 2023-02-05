/* eslint-disable */
// @ts-nocheck
(function ($) {
  jQuery(document).ready(function ($) {
    let userAgent = window.navigator.userAgent,
        platform = window.navigator.platform,
        macosPlatforms = ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'],
        windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
        iosPlatforms = ['iPhone', 'iPad', 'iPod'],
        os = null;

    if (macosPlatforms.indexOf(platform) !== -1) {
        os = 'Mac OS';
        $(".banner-platform").text(" MacOS");
        $(".banner-btn").attr("href", "https://lingvanex-downlod.s3.eu-central-1.amazonaws.com/LingvanexMacOS.dmg?position=banner");
    } else if (iosPlatforms.indexOf(platform) !== -1) {
        os = 'iOS';
        $(".banner-platform").text(" iOS");
        $(".banner-btn").attr("href", "https://apps.apple.com/app/apple-store/id1254981151?pt=118725202&ct=site&mt=8&position=banner");
    } else if (windowsPlatforms.indexOf(platform) !== -1) {
        os = 'Windows';
        $(".banner-platform").text(" Windows");
        $(".banner-btn").attr("href", "https://lingvanex-downlod.s3.eu-central-1.amazonaws.com/LingvanexWindows.msi?position=banner");
    } else if (/Android/.test(userAgent)) {
        os = 'Android';
        $(".banner-platform").text(" Android");
        $(".banner-btn").attr("href", "https://play.google.com/store/apps/details?id=com.nordicwise.translator&position=banner&referrer=utm_source%3Dsite%26utm_campaign%3D09112021site");
    } else if (!os && /Linux/.test(platform)) {
        os = 'Linux';
        $(".banner-platform").text(" Windows");
        $(".banner-btn").attr("href", "https://lingvanex-downlod.s3.eu-central-1.amazonaws.com/LingvanexWindows.msi?position=banner");
    }
    return os;
});
})(jQuery);
