import subprocess


ALLOWED_APPLICATIONS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
}


def open_application(application: str) -> dict:
    application = application.strip().lower()

    if application not in ALLOWED_APPLICATIONS:
        return {
            "success": False,
            "message": (
                f"Application '{application}' is not in the allowed list"
            ),
        }

    try:
        subprocess.Popen(ALLOWED_APPLICATIONS[application])

        return {
            "success": True,
            "application": application,
            "message": f"{application} launch command executed",
        }

    except Exception as error:
        return {
            "success": False,
            "application": application,
            "message": str(error),
        }