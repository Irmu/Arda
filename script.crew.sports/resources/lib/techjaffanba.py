
import base64, codecs
thecrew = 'aW1wb3J0IHJlcXVlc3RzDQppbXBvcnQgcmUNCmZyb20gYnM0IGltcG9ydCBCZWF1dGlmdWxTb3VwDQoNCm5iYV9nYW1lcyA9IFtdDQoNCmRlZiBnZXRfbmJhKCk6DQogICAgdXNlckFnZW50ID0gJ01vemlsbGEvNS4wIChXaW5kb3dzIE5UIDYuMTsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzc2LjAuMzgwOS4xMzIgU2FmYXJpLzUzNy4zNicNCiAgICBodG1sID0gcmVxdWVzdHMuZ2V0KCdodHRwOi8vY3JhY2tzdHJlYW1zLmNvbS9uYmFzdHJlYW1zLycsaGVhZGVycz17J3VzZXItYWdlbnQnOnVzZXJBZ2VudH0pDQogICAgc291cCA9IEJlYXV0aWZ1bFNvdXAoaHRtbC5jb250ZW50LCdodG1sLnBhcnNlcicpDQogICAgYSA9IHNvdXAuZmluZF9hbGwoJ2EnLGNsYXNzXz17J2J0biBidG4tZGVmYXVsdCBidG4tbGcgYnRuLWJsb2NrJ30pDQogICAgZm9yIGRhdGEgaW4gYToNCiAgICAgICAgdGl0bGUgPSBkYXRhLmZpbmQoJ2g0JyxjbGFzc189eydtZWRpYS1'
doesnt = 'bMJSxnJ5aW30cYaEyrUDAPvNtVPNtVPNtqTy0oTHtCFO0nKEfMF5yozAiMTHbW2SmL2ycWljanJqho3WyWlxAPvNtVPNtVPNtqTy0oTHtCFO0nKEfMF5xMJAiMTHbW3I0Mv04WljanJqho3WyWlxAPvNtVPNtVPNtozWuK2quoJImYzSjpTIhMPu7W3EcqTkyWmc0nKEfMK0cQDbAPvNtVPOlMKE1pz4tozWuK2quoJImQDbAPvAjpzyhqPuaMKEsozWuXPxcQDcmqUWyLJ0tCFOoKD0XQDcxMJLtM2I0K3A0pzIuoFuaLJ1yXGbAPvNtVPOuM2IhqPN9VPqAo3ccoTkuYmHhZPNbI2yhMT93plOBIPN2YwR7VSqcowL0BlO4AwDcVRSjpTkyI2IvF2y0YmHmAl4mAvNbF0uHGHjfVTkcn2HtE2Iwn28cVRAbpz9gMF83Av4jYwZ4ZQxhZGZlVSAuMzSlnF81ZmphZmLaQDbtVPNtnUEgoPN9VUWypKIyp3EmYzqyqPtanUE0pQbiY2AlLJAep3ElMJSgpl5wo20iozWup3ElMJSgpl8aYTuyLJEypaZ9rlq1p2IlYJSaMJ50WmcuM2IhqU0cQDbtVPNtp291pPN9VRWyLKI0nJM1oSAiqKNbnUEgoP5wo250MJ50YPqbqT1fYaOupaAypvpcQDbtVP'
do = 'AgYSA9IHNvdXAuZmluZF9hbGwoJ2EnLGNsYXNzXz17J2J0biBidG4tZGVmYXVsdCBidG4tbGcgYnRuLWJsb2NrJ30pDQogICAgZm9yIGRhdGEgaW4gYToNCiAgICAgICAgdGl0bGUgPSBkYXRhLmZpbmQoJ2g0JyxjbGFzc189eydtZWRpYS1oZWFkaW5nJ30pLnRleHQNCiAgICAgICAgdGl0bGUgPSB0aXRsZS5lbmNvZGUoJ2FzY2lpJywnaWdub3JlJykNCiAgICAgICAgdGl0bGUgPSB0aXRsZS5kZWNvZGUoJ3V0Zi04JywnaWdub3JlJykNCiAgICAgICAgaWYgZ2FtZSBpbiB0aXRsZToNCiAgICAgICAgICAgIHVybCA9IGRhdGFbJ2hyZWYnXQ0KICAgICAgICAgICAgaHRtbCA9IHJlcXVlc3RzLmdldCh1cmwsaGVhZGVycz17J3VzZXItYWdlbnQnOmFnZW50fSkuY29udGVudA0KICAgICAgICAgICAgc291cCA9IEJlYXV0aWZ1bFNvdXAoaHRtbCwnaHRtbC5wYXJzZXInKQ0KICAgICAgICAgICAgZnJhbWUgPSBzb3VwLmZpbmQoJ2lmcmFtZScpDQogICAgICAgICAgICBpZiBmcmFtZToNCiAgICAgICAgICAgICAgICBmc'
drama = 'zSgMFN9VTMlLJ1yJlqmpzZaKD0XVPNtVPNtVPNtVPNtVPNtVT1up3EypvN9VUWypKIyp3EmYzqyqPuzpzSgMFkbMJSxMKWmCKfapzIzMKWypvp6qKWfsFxhL29hqTIhqN0XVPNtVPNtVPNtVPNtVPNtVUAiqKNtCFOPMJS1qTyzqJkGo3IjXT1up3EypvjanUEgoP5jLKWmMKVaXD0XVPNtVPNtVPNtVPNtVPNtVT0mqGttCFOlMF5wo21jnJkyXPqmo3IlL2H6VPVbYvf/XFVaYUWyYxECIRSZGPxhMzyhMTSfoPumqUVbp291pP5jpzI0qTyzrFxcQDbtVPNtVPNtVPNtVPNtVPNtoGA1BPN9VT0mqGuoZS0APvNtVPNtVPNtVPNtVPNtVPOgZ3H4VQ0toGA1BPNeVPq8pzIzMKWypw0aVPftMaWuoJHAPvNtVPNtVPNtVPNtVPNtVPOmqUWyLJ0hLKOjMJ5xXUfaqTy0oTHaBaEcqTkyYPqmqUWyLJ0aBz0mqGu9XD0XVPNtVPNtVPNtVPNtVPNtVTWlMJSeQDbtVPNtVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtVPNtVTWlMJSeQDbtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPOwo250nJ51MD0XQDbtVPNtpzI0qKWhVUA0pzIuoD0X'
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))