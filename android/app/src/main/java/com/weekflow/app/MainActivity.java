package com.weekflow.app;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.appcompat.app.AppCompatActivity;

/**
 * 原生 WebView 壳：加载 assets/index.html（WeekFlow 前端应用）。
 * 不引入任何第三方混合框架，纯 Android SDK，最小体积、最稳定。
 */
public class MainActivity extends AppCompatActivity {

    private WebView webView;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webview);
        WebSettings ws = webView.getSettings();

        // —— 功能开关 ——
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);                 // 关键：启用 localStorage / IndexedDB（App 数据持久化）
        ws.setAllowFileAccess(true);                   // 允许加载 assets 内的 file:// 资源
        ws.setAllowFileAccessFromFileURLs(true);
        ws.setAllowUniversalAccessFromFileURLs(true);
        ws.setLoadWithOverviewMode(true);
        ws.setUseWideViewPort(true);
        ws.setBuiltInZoomControls(false);
        ws.setDisplayZoomControls(false);
        ws.setCacheMode(WebSettings.LOAD_DEFAULT);
        // 字体不小于 16px，避免 Android 聚焦 input 时自动缩放（前端 CSS 已统一 16px）
        ws.setTextZoom(100);

        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());

        // 离线优先：直接加载本地 assets，无需联网即可打开全部 UI
        webView.loadUrl("file:///android_asset/index.html");
    }

    /**
     * Android 返回键逻辑：
     * 1) 有浮层 → 关闭最上层浮层
     * 2) 否则若 WebView 能后退 → 后退
     * 3) 否则退出 App
     * 通过前端暴露的 window.__mobileHasOverlay / __mobileCloseTop 协同。
     */
    @Override
    public void onBackPressed() {
        if (webView == null) { finish(); return; }
        webView.evaluateJavascript(
                "(function(){ if(window.__mobileHasOverlay && window.__mobileHasOverlay()){ window.__mobileCloseTop(); return 'handled'; } return 'none'; })()",
                value -> {
                    if (!"handled".equals(value)) {
                        if (webView.canGoBack()) webView.goBack();
                        else finish();
                    }
                }
        );
    }
}
