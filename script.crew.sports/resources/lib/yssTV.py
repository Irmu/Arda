
import base64, codecs
thecrew = 'aW1wb3J0IHJlcXVlc3RzCmZyb20gYnM0IGltcG9ydCBCZWF1dGlmdWxTb3VwCmltcG9ydCByZQppbXBvcnQgYmFzZTY0CgpnYW1lID0gW10KZGVmIGdldF9nYW1lcygpOgogICAgdXJsID0gImh0dHA6Ly95b3Vyc3BvcnRzLnN0cmVhbS9nYW1lcy5qcz94PTE1Nzg4NDYwMzEiCiAgICBodG1sID0gcmVxdWVzdHMuZ2V0KHVybCkuY29udGVudAogICAgc291cCA9IEJlYXV0aWZ1bFNvdXAoaHRtbCwnaHRtbC5wYXJzZXInKQogICAganNvbkxpc3QgPSByZS5jb21waWxlKCJ0dj0oLis/KV07IixyZS5ET1RBTEwpLmZpbmRhbGwoc3RyKHNvdXAucHJldHRpZnkpKQogICAganNvbkxpc3QgPSBqc29uTGlzdFswXQogICAganNvbkxpc3QgPSBqc29uTGlzdC5yZXBsYWNlKCJbIiwiIikKICAgIHRpdGxlcyA9IHJlLmNvbXBpbGUoImNoYW46JyguKz8pJyIscmUuRE9UQUxMKS5maW5kYWxsKGpzb25MaXN0KQogICAgdXJsID0gcmUuY29tcGlsZSgidXJsOicoLis/KSciLHJlLkRPVEFMTCkuZ'
doesnt = 'zyhMTSfoPudp29hGTymqPxXVPNtVUOlnJ9lVQ0tVzu0qUN6Yl95o3Ilp3OipaEmYaA0pzIuoF9fnKMyC3L9VtbtVPNtnJ5xMKttCFOfMJ4bqTy0oTImXDbtVPNtnFN9VQNXVPNtVUqbnJkyVPucVQjtnJ5xMKtcBtbtVPNtVPNtVUEcqTkyVQ0tqTy0oTImJ2yqPvNtVPNtVPNtoTyhnlN9VUOlnJ9lVPftqKWfJ2yqPvNtVPNtVPNtM2SgMF5upUOyozDbrlW0nKEfMFV6qTy0oTHfVzkcozfvBzkcozg9XDbtVPNtVPNtVTxtXm0tZDbXVPNtVUWyqUIlovOaLJ1yPtbXp3ElMJSgVQ0tJ10XPtcxMJLtM2I0K3A0pzIuoFufnJ5eXGbXVPNtVTSaMJ50VQ0tVx1irzyfoTRiAF4jVPuKnJ5xo3qmVR5HVQRjYwN7VSqcowL0BlO4AwDcVRSjpTkyI2IvF2y0YmHmAl4mAvNbF0uHGHjfVTkcn2HtE2Iwn28cVRAbpz9gMF83BF4jYwZ5AQHhZGR3VSAuMzSlnF81ZmphZmLvPvNtVPObqT1fD29hqTIhqPN9VUWypKIyp3EmYzqyqPufnJ5eYPObMJSxMKWmCKfvqKAypv1uM2IhqPV6VTSaMJ50sFxhL29hqT'
do = 'VudAogICAgc291cCA9IEJlYXV0aWZ1bFNvdXAoaHRtbENvbnRlbnQsICdodG1sLnBhcnNlcicpCiAgICBpZnJhbWUgPSByZS5jb21waWxlKCc8aWZyYW1lIGFsbG93ZnVsbHNjcmVlbj0iIiBhbGxvd3RyYW5zcGFyZW5jeT0iIiBmcmFtZWJvcmRlcj0iMCIgaGVpZ2h0PSIxMDAlIiBzY3JvbGxpbmc9Im5vIiBzcmM9IiguKz8pIicscmUuRE9UQUxMKS5maW5kYWxsKHN0cihzb3VwLnByZXR0aWZ5KSkKICAgIGlmIGlmcmFtZToKICAgICAgICBpZnJhbWUgPSBpZnJhbWVbMF0KICAgICAgICBodG1sQ29udGVudCA9IHJlcXVlc3RzLmdldChpZnJhbWUsIGhlYWRlcnM9eyJ1c2VyLWFnZW50IjogYWdlbnQsICJyZWZlcmVyIjogbGlua30pLmNvbnRlbnQKICAgICAgICBzb3VwID0gQmVhdXRpZnVsU291cChodG1sQ29udGVudCwgJ2h0bWwucGFyc2VyJykKICAgICAgICBjb250ZW50ID0gc3RyKHNvdXAucHJldHRpZnkpCiAgICAgICAgZW5jcnlwdCA9IHJlLmNvbXBpbGUoImF0b2JcKC4'
drama = 'eC1jcVvjtpzHhER9HDHkZXF5znJ5xLJkfXTAioaEyoaDcPvNtVPNtVPNtnJLtMJ5wpayjqQbXVPNtVPNtVPNtVPNtMJ5wpayjqPN9VTIhL3W5pUEoZS0XVPNtVPNtVPNtVPNtMJ5wpayjqPN9VTIhL3W5pUDhpzIjoTSwMFtvLKEiLvtaVvjtVvVcYaWypTkuL2HbVvpcVvjtVvVcPvNtVPNtVPNtVPNtVTEyL3W5pUDtCFOvLKAyAwDhLwL0MTIwo2EyXTIhL3W5pUDcPvNtVPNtVPNtVPNtVUA0pzIuoF5upUOyozDbrlW0nKEfMFV6VPWoD09ZG1Vto3WwnTyxKFcoY0ACGR9FKFOoDy1oD09ZG1Vtq2ucqTIqHTkurFOGqUWyLJ1oY0ACGR9FKIfiDy0tJ0ACGR9FVT9lL2ucMS0dJl9QG0kCHy0vYNbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNvoTyhnlV6VTEyL3W5pUDtXlNvsSImMKVgDJqyoaD9VvNeVTSaMJ50VPftVvMFMJMypzIlCFVtXlOcMaWuoJI9XDbtVPNtVPNtVTIfp2H6PvNtVPNtVPNtVPNtVUOup3ZXVPNtVTIfp2H6PvNtVPNtVPNtpTSmpjbXVPNtVUWyqUIlovOmqUWyLJ0='
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))