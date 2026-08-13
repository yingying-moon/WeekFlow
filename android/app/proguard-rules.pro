# 保留 WebView 相关（release 未开启混淆，这里仅占位）
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
