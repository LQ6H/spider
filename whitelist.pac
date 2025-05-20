// pac-proxy.js
function FindProxyForURL(url, host) {
  // 定义代理服务器（假设你的代理是 socks5://127.0.0.1:7890）
  var proxy = "SOCKS5 127.0.0.1:1080";

  // 判断是否匹配 example.com 或其子域名
  if (shExpMatch(host, "*.ipinfo.io") || shExpMatch(host, "ipinfo.io")) {
    return proxy;
  }

  // 默认直连
  return "DIRECT";
}
