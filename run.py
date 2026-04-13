from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) # nosemgrep: python.flask.security.audit.app-run-param-config.avoid_app_run_with_bad_host # nosec B104
