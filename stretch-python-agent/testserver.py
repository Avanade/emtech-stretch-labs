from pyngrok import ngrok

https_tunnel = ngrok.connect(bind_tls=True)
print("The HTTPs tunnel is established. Push CTRL+C to terminate.")
print(https_tunnel)
ngrok_process = ngrok.get_ngrok_process()

try:
    ngrok_process.proc.wait()
except KeyboardInterrupt:
    print("Shutting down server.")

    ngrok.kill()