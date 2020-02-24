
import base64, codecs
thecrew = 'DQppbXBvcnQgYmFzZTY0LCBjb2RlY3MNCnRoZWNyZXcgPSAnRFFwcGJYQnZjblFnWW1GelpUWTBMQ0JqYjJSbFkzTU5DblJvWldOeVpYY2dQU0FuWVZjeGQySXpTakJKU0Vwc1kxaFdiR016VW5wRVVYQndZbGhDZG1OdVVXZGpiVlZPUTIxYWVXSXlNR2RaYmswd1NVZHNkR05IT1hsa1EwSkRXbGRHTVdSSGJHMWtWM2hVWWpOV2QwUlJjSEJpV0VKMlkyNVJaMk16YkhwRVVYQnRZMjA1ZEVsSVNteGpNamt4WTIxT2JHTjVOWE5oVjBsbllWY3hkMkl6U2pCSlIwNXRZekpPZVZsWVFteEVVVzlxWVZjeGQySXpTakJKU0docFlsZE9ibVJYYTA1RFp6QkxXVmRrYkdKdVVXZFFVMEZ1VkZjNU5tRlhlSE5aVXpneFRHcEJaMHRHWkhCaWJWSjJaRE5OWjFSc1VXZE9hVFI0VDNsQ1dHRlhOREpPUkhOblpVUlpNRXRUUWtKalNFSnpXbFprYkZscmRIQmtRemd4VFhwamRVMTZXV2RMUlhSSlZrVXhUVXhEUW5OaFYzUnNTVVZrYkZreWRIWkxVMEpFWVVoS2RtSlhWWFpPZWxsMVRVTTBlazlFUVRWTWFrVjZUV2xDVkZsWFdtaGpiV3QyVGxSTk0weHFUVEpLZHpCTFJGRndibGxYTVd4WU1uaHdZek5SWjFCVFFtSllVVEJMUkZGd2ExcFhXV2RhTWxZd1dESmthR0pYVm5wTFEyczJSRkZ2WjBsRFFXZGpNazU1V1ZoQ2JHTnBRVGxKUjA1dFl6Sk9lVmxZUW14TWJVNTVXbGRHTUZwV09YcFpNMHBvWTBkV2VVdERhMDVEYVVGblNVTkNiMlJITVhOSlJEQm5ZekpPZVZsWVFteGphVFZ1V2xoUmIwb3lhREJrU0VFMlRIazVNMlF6WTNWak0xSjVXbGRHZEZwWFJucGtRelZ6WVZoYWJFd3pUakJqYlZab1lsaE5kbVJ0T1hOaVIxWTFXVzFHYzJKRE9HNU1SMmhzV1ZkU2JHTnVUVGxsZVdReFl6SldlVXhYUm01YVZ6VXdTbnB3YUZveVZuVmtTREJ3VEcxT2RtSnVVbXhpYmxGT1EybEJaMGxEUW5waU0xWjNTVVF3WjFGdFZtaGtXRkp3V201V2MxVXlPVEZqUTJodlpFY3hjMHhEWkc5a1J6RnpURzVDYUdOdVRteGphV053UkZGdlowbERRV2RaVTBFNVNVaE9kbVJZUVhWYWJXeDFXa1k1YUdKSGQyOUtNbEp3WkdsamMxa3llR2hqTTA1bVVGaHpibGt5T1hOTVZ6RnJURlJOWnljTkNtUnZaWE51ZENBOUlDZE1NamxtV1V0MWJWbEhjSFJ3VkZONFRWUjVhRTFzTVdoeFNtdG1WbFZGZVhKVlJHZHZWRWw2Y1ZCeE9WaEVNRmhXVUU1MFZsUk5hWEIyVDNoTVMwVjFWbFI1YUZaVVVqWlJSR0owVmxCT2RGWlEnDQpkb2VzbnQgPSAnR2FFSklISXdwSUVlcklNRVpVRUFJU1pqR1JMMXJ6NVhBS3VMSFVTNG94Z1pMSXlIREpNWkYwU2dGMjBrQTFwbUVLeVpGd091cDBNNG5VU0hGR0'
doesnt = 'IeE3qCGRy5G0WkH01RE2SSFxuFBKIUHzWepxuzoT4lDJcnZRIvE1WaD254ZIuOF3IZFHcAqKOWEGInIQyVEyEGHRkVFKqjFHIypxy5AxMXqIcnq3x0E0uAZRkVn1yRF3SbEzS1qHcWG2gZZQOfDHc5naW4qKIXHxjkpyVkJREXrHSWHaI2FJ1OI1cFZGWnHHIYo1EwqJ94L2ghIQugFGA5F29IrQIXHxEdFyAGHxkuEHcVHwHjpSIwI1cIH1yWZaIXFIIGZJ8jL1qjZwyVpxbkn0q3G0kVFRI2pGACFHxlDJyZFRI2E0qKI1cFMzkjF0ycEau5M0cGGmEZZIAFGUuGERkVHzcjIJAKpHb5IRq3rHcVZaSeFRuSqxEWGmMSF3yOpKt5qHqVM1AjZ05gEHceDHM5DJSXH0IepHb5JRMHDIOkHH9ZFKyCDaSGGHyRF3SdpayOMRqVM0ckHxSHEmAkDHkVHmAjIJAUoatkIRSYpJclrUxkpRySI3NmGzkRFzgnEwN5AKOIGGOZZIAFGTSSFxuFAGOirHyGGGV5ERq3rHcWFSZmpSIwE254ZIyWraIOJau4nxcGG2gZLIAWEHcwHUS3qJAjE0SeJwS5qHEUG2clrUxkomOwI3SYGz1SIUIcFII4oRqVGQIiF1AWFGA5JxM3H2qXE0SOoxb5FT4mrJkTrKRkomSSMT5WpJMhZyqOEayOARqVM0giFRSMGKcGn0LjHmIjIHkepHtjoRMXqJgVIH4lE1Wwn3WXBKISE3yZEKqWZ29gIwSnHwSLDHqCEHIHImOWrH9PpIIBoRWUH2cVHwD1FKyKF3WVn1yTE09bEatjn28kDH9hF1AME3cKnRyVFJSiZH9xGRb1FHIXpJyVHHyxE1WaF29VZIyWryAZEISCGRy5G0WkH01VFTSSHHI4BJqioHSKoay5AxqXDJylrRygE1WwMH15qHEjF3IbEwOeqHcWEH9ArTgMERbkJJ9UHwAWoIqCoxb5EScXpHSVHH9aI2bjJR1HBUEQEx5uExukDaS6I1SnE0I3pxqBoHMVqIOhH2AIFTSCqz9XDGOZrwIXpQWKHHE3G25XIUEdE1AkAT9GL2uVFwI6FQWaDxDlrH9AZUyEEUbkqybjrJSXrUSHJyA5E0EuG3MhFSqvEmWjnxLjrISRFaSKEQOGLHMVDIOnISAZFTSOoxtjHwITFUSToyESIHIYFJ5iFzfkFauOLJ95L1IiHIqLpxg1MRk4pIElryceDyS5rKWXETcXrKSHpIWvoIcIG1cirIqzGHu1EHq4DJARFaSKEQOGLHMVDH9AZyAJEaceoz5VHwITFUSToyESIHIYFH1WLHSbGRu1JT9GL2AAIRIFFRb5LHMVDH9AZUyEERckI0DjAGZaQDcxolN9VPqMZwSmMSqFETSRDzuKExc6I2kBATVlGaEJoGSZIIEPGSAIGxWnZTkRHIqxFyRjEaSnIJEYMRMerIcREzuIryMTJIMxE2ZlFKyMZwyZIKcIq1qfnT9AE1W0Lxq4n01fJwIGZR5eHz1BqIAhJzcuI056H1IbG01UGaOuE3EnI0MXo1ZkGaWHn05jHIqxFyRjEz5GIH5PJwWTJSqKMTSAn1bjI2kBD2AUFaOEnxWbI0MXryqfHaMHn05jHIqxFyRjEz5GIH5PJwOfESSKMRcG'
do = 'Rlo1WWtOQk9VbEhhSGxhVjFsT1EybEJaMGxEUVdkSlEwRm5TVU5CWjBsSGFEQmlWM2RuVUZOQ2Vsa3pTbWhqUjFaNVRHMWtiR1JEYURGamJYZHpZVWRXYUZwSFZubGplakUzU2pOV2VscFlTWFJaVjJSc1ltNVJiazl0Um01YVZ6VXdabE5yZFZreU9YVmtSMVoxWkVFd1MwbERRV2RKUTBGblNVTkJaMGxEUVdkak1qa3hZME5CT1VsRlNteFpXRll3WVZkYU1XSkdUblprV0VGdllVaFNkR0pEZDI1aFNGSjBZa00xZDFsWVNucGFXRWx1UzFFd1MwbERRV2RKUTBGblNVTkJaMGxEUVdkYWJrcG9ZbGRWWjFCVFFucGlNMVozVEcxYWNHSnRVVzlLTW14dFkyMUdkRnBUWTNCRVVXOW5TVU5CWjBsRFFXZEpRMEZuU1VOQ2NGcHBRbTFqYlVaMFdsUnZUa05wUVdkSlEwRm5TVU5CWjBsRFFXZEpRMEZuU1VOQ2JXTnRSblJhVTBFNVNVZGFlVmxYTVd4WGVXUjZZMjFOYmxoUk1FdEpRMEZuU1VOQlowbERRV2RKUTBGblNVTkJaMGxITVdoak0xSnNZMmxCT1NjTkNtUnlZVzFoSUQwZ0oxWlZRWGR3ZWxOcVRVdFdhRTB5U1RCWVZFMXNURW94ZVZsVWRYbE1Ta1Y1Y0dGYU9YSnNjV3hOU2sxNWNIcEpiRmR0WXpGd2VtczVXRVkxZDI4eU5UQk5TalV3VVVSaWRGWlFUblJXVUU1MFZsQk9kRlpRVG5SV1VFNTBjREk1TVhCUVRqbFdVbGQ1VEV0Sk1HNUtUVEZ2VTBGcGNVdE9ZbTlLVTIxeFZFbHNXVkJ4WW5GVU1XWlpZVTkxY0dGQmVYQjJjR05SUkdKMFZsQk9kRlpRVG5SV1VFNTBWbEJPZEZaUVRuUnZSMEV4UWxCT09WWlZWM2xaZWtGcGIwdFBZMjlVU0dKWE0wRnBjVXRYZDAxSFluUldkblJvV0cwNFkxWjJjR1p3ZWtob1JWSTVTRVJJYTFwWVJqVjZia28xZUV4S2EyWllWVUV3Y0haMWJXOHpTV3BaWVU5c1RVdEZNRzVLVFRWWVJuaEJVSFpPZEZaUVRuUldVRTUwVmxCT2RGWlFUblJXVUU5bldqTklORlpSTUhSdlIwRXhRbE5tYWt0RU1GaFdVRTUwVmxCTycNCmRyYW1hID0gJ3FTTURHYUVKSFI1MEl5T0JxU01IWlQxa0UzRTBEME1DTTFibUZRRUpIVE0wSXlPa0JSeVlES3lqcXdTQ0dHV1duVVNFWlRTTG9SOTFHR1dXblVTREd6SUtvUjFUR0hjQXJLTzZGSmtRRWFPMEpUa0NyYU82SDJxQUVRT0xJeU9CcVNNREdhRUpIUjUwSXlPQnFTTURHYUVKSUhSanBVY1dxSjlUQUtJaklIOTVvM2NSTGFXZnBHT2hGMEl6R0hNakFhU0hyR09pSVJ1ekltQU9aVU82RktJaUVhTjJvMHFPWkhXSVpUQUVFVFcwSXlPQnFTTURHYUVKSFI1MEl5T0JxU01ER2FFWkxJcTVHUmN6RElPMkdhRUpIUjUwSXlPQnFTTURHYUVKSVJ5enBRV1ZBeVNSTGFFSkhSNTBJeU9CcVNNRE'
drama = 'quEHcVHwHjFKyCDaSFn3IWZ3ynEacAG0uIGHWkH01RE2SSFxuFAGOUFTAyo0tkIHk4H0EkrQHjFKyCDaSGGHEULHIXFSV1ZRy5EH9hFwy1EHcOnHkVrGIVFRI2ERyCZxquEHcVHwyzE0uaH1cYGmMOIHIdJwOWMxqVL0qAZIAFGUuGEUSEG0kWq0SQo1D1JRSUG0kWIIZ1pRynAJ9YH0yWZ3ynEaqCqxygG0SWZUR0FQSwIHtmqKIXHx00ERyCZRAUZTSEETAfGHgOnx1XDGOJHGO0ImSeARSgI3OlHH16F1I0Z0SGnmEnoIAjpySnoIqdZSukF0S1o3cSAJ8mFUEQEx95pKcGMyuDpKOlHKNjF1I0ZxWGnmEOq0yjpySZoHgIqQAnrJf0DKqWpUWEpQAKoUu0JTkCrKS6H2MLHUSjpySZoHgIqQWArJf0DKqSpUWEGQSYIKDlJwSeARSgDKOlHIq5F1I0ZxSGnmEOq0yjpySZoHgIqQWArJf0DKqSpUWEGQSYIKEfDyAeARS3EKOlHH16F1I0ZxSWnmEOoHSjpySArHgIqQAOH2f0JacOpUWEIzcYIKDmJayeARS3FKOlHKOgF1I0Z1cGnmEOq0yjpySZoHgIqQAOH2f0Jaq4LIuTGzIJIRxlGRcdLypknmEOq0IjpySAryqfrUELoR95pKcGMyuDpKOlHHkgF1I0Zx15nmEOq0IjpySZZHgIqQWnZJf0DJ1OpUWEI3yYIKDlDIAeARS3FKOlHHkgF1I0Zx15nmEOq0IjpySZZHgIqTkPH2f0DKqSpUWEpTkYIKDlJxyeARS6EKOlHHkeF1I0oRjknmEnq09jpySjoRgIqQWOFJf0DJ1OpUWEpTcYIKDlDHyeARS3DKOlHKNjF1I0oRWTpTAEETA5pKcGMyuHDJyiF09wo1EVLxk6H21AE0jjJKcJZxSHEKyZZwy4GHM1rKS6H2MLHUSjpySjZHgIqQAnZJf0DKqGpUWEGKyYIKDlDIAeARSgrKOlHH16F1I0Z0STpTALEzcuD1IOZUO6rJuAoGEuJIOkrKWHFKqKoUuwWj0XpzImpTIwqPN9VPqprQplKUt2Myk4AmEprQZkKUtmZlpAPaImLJ5xrJ91VQ0tMKMuoPtaKUt3ASk4AwuprQL1KUt2Z1k4AmWprQL1KUt3AlpcVPftMKMuoPtaKUt2Z1k4AzMprQL0KUt2AIk4AwAprQpmKUtlMIk4AwEprQL1KUt2Z1k4AzMprQL0KUt2AIk4ZwuprQL0KUt2Myk4AwIprQpmKUt2MIk4AmEprQWwKUtlZSk4AmWprQL1KUt3Z1k4AmOprQL1KUt2Z1k4AmEprQV5WlxtXlOyqzSfXPqprQL0KUt2MvpcVPftMKMuoPtaKUt2Z1k4AzMprQL0KUt2AIk4AwAprQpmKUtlMIk4AwEprQL1KUt2Z1k4AzMprQL0KUt2AIk4ZwuprQL0KUt3Zyk4AwSprQMxKUt2ZIk4ZzAprQVjKUt3Zyk4AwIprQpmKUt3ZSk4AwIprQLmKUt3ASk4ZwxaXD0XMKMuoPuwo21jnJkyXTWup2H2AP5vAwExMJAiMTHbMKMuoPtaKUt3AIk4AmAprQLkKUt2MIk4AwEprQp5KUt2Myk4AmHaXFxfWmkmqUWcozp+WljaMKuyLlpcXD=='
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))