import base64
import logging
import subprocess  # nosec B404

# EPAM Colors
COLOR_GRAVEL = "#464547"
COLOR_SCOOTER = "#39c2d7"
COLOR_WHITE = "white"

POWERSHELL_WARNING_SCRIPT = r"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "VPN Warning"
$form.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::None
$form.TopMost = $true
$form.BackColor = [System.Drawing.ColorTranslator]::FromHtml("#464547")
$form.Width = 450
$form.Height = 120
$form.StartPosition = "Manual"
$form.ShowInTaskbar = $false

$screenWidth = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea.Width
$form.Location = New-Object System.Drawing.Point(($screenWidth - 450 - 20), 20)

# Side Strip
$strip = New-Object System.Windows.Forms.Panel
$strip.Width = 10
$strip.Dock = "Left"
$strip.BackColor = [System.Drawing.ColorTranslator]::FromHtml("#39c2d7")
$form.Controls.Add($strip)

# Label
$label = New-Object System.Windows.Forms.Label
$label.Text = "VPN DISCONNECTED!`nAccessing Windows App from unauthorized region."
$label.ForeColor = "White"
$label.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$label.TextAlign = "MiddleCenter"
$label.Dock = "Fill"
$form.Controls.Add($label)

$form.ShowDialog()
"""

POWERSHELL_INPUT_SCRIPT_TEMPLATE = r"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "{title}"
$form.Size = New-Object System.Drawing.Size(300, 150)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false
$form.MinimizeBox = $false
$form.TopMost = $true

$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10, 20)
$label.Size = New-Object System.Drawing.Size(280, 20)
$label.Text = "{prompt}"
$form.Controls.Add($label)

$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Location = New-Object System.Drawing.Point(10, 50)
$textBox.Size = New-Object System.Drawing.Size(260, 20)
$textBox.Text = "{default_value}"
$form.Controls.Add($textBox)

$okButton = New-Object System.Windows.Forms.Button
$okButton.Location = New-Object System.Drawing.Point(100, 80)
$okButton.Text = "OK"
$okButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $okButton
$form.Controls.Add($okButton)

$result = $form.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK) {{
    Write-Output $textBox.Text
}} else {{
    Write-Output "CANCELLED"
}}
"""


class WarningWindow:
    def __init__(self):
        self.process = None

    def show(self):
        if self.process is None or self.process.poll() is not None:
            logging.info("Showing Warning Window (PowerShell)")
            try:
                script_bytes = POWERSHELL_WARNING_SCRIPT.encode("utf-16le")
                encoded_command = base64.b64encode(script_bytes).decode("utf-8")

                # CREATE_NO_WINDOW = 0x08000000
                self.process = subprocess.Popen(  # nosec B603 B607
                    [
                        "powershell",
                        "-NoProfile",
                        "-NonInteractive",
                        "-EncodedCommand",
                        encoded_command,
                    ],
                    creationflags=0x08000000,
                )
            except Exception as e:
                logging.error(f"Failed to start warning window: {e}")

    def hide(self):
        if self.process and self.process.poll() is None:
            logging.info("Hiding Warning Window")
            try:
                self.process.terminate()
                self.process = None
            except Exception as e:
                logging.error(f"Failed to hide warning window: {e}")

    def start(self):
        pass

    def stop(self):
        self.hide()


def get_input(title, prompt, default=""):
    try:
        script = POWERSHELL_INPUT_SCRIPT_TEMPLATE.format(
            title=title, prompt=prompt, default_value=default
        )

        encoded_command = base64.b64encode(script.encode("utf-16le")).decode("utf-8")

        result = subprocess.run(  # nosec B603 B607
            ["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded_command],
            capture_output=True,
            text=True,
            creationflags=0x08000000,
        )

        output = result.stdout.strip()
        if output == "CANCELLED" or not output:
            return None
        return output
    except Exception as e:
        logging.error(f"Error getting input: {e}")
        return None
