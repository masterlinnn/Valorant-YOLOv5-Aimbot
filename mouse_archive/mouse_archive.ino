////////////////////////////////////////////////////////////////////////////////////
float aimDelay = 3.0;
float aimDeceleration = 0.04;
float sensitivity = 6.07315;
////////////////////////////////////////////////////////////////////////////////////

float aimDelayDefault = aimDelay;

#include <hidboot.h>
#include <usbhub.h>
#include <Mouse.h>

// Satisfy the IDE, which needs to see the include statment in the ino too.
#ifdef dobogusinclude
#include <spi4teensy3.h>
#endif
#include <SPI.h>

String data = "";

int indexX, indexY, indexAst, indexState, x, y;
String state;

class MouseRptParser : public MouseReportParser
{
  protected:
    void OnMouseMove  (MOUSEINFO *mi);
    void OnLeftButtonUp (MOUSEINFO *mi);
    void OnLeftButtonDown (MOUSEINFO *mi);
    void OnRightButtonUp  (MOUSEINFO *mi);
    void OnRightButtonDown  (MOUSEINFO *mi);
    void OnMiddleButtonUp (MOUSEINFO *mi);
    void OnMiddleButtonDown (MOUSEINFO *mi);
};
void MouseRptParser::OnMouseMove(MOUSEINFO *mi)
{
  Mouse.move(mi->dX, mi->dY, 0);
};
void MouseRptParser::OnLeftButtonUp (MOUSEINFO *mi)
{
  Mouse.release();
};
void MouseRptParser::OnLeftButtonDown (MOUSEINFO *mi)
{
  Mouse.press();
};
void MouseRptParser::OnRightButtonUp  (MOUSEINFO *mi)
{
  Mouse.release(MOUSE_RIGHT);
};
void MouseRptParser::OnRightButtonDown  (MOUSEINFO *mi)
{
  Mouse.press(MOUSE_RIGHT);
};
void MouseRptParser::OnMiddleButtonUp (MOUSEINFO *mi)
{
  Mouse.release(MOUSE_MIDDLE);
};
void MouseRptParser::OnMiddleButtonDown (MOUSEINFO *mi)
{
  Mouse.press(MOUSE_MIDDLE);
};

USB Usb;
USBHub Hub(&Usb);
HIDBoot<USB_HID_PROTOCOL_MOUSE> HidMouse(&Usb);

MouseRptParser Prs;

void setup()
{
  delay(200);
  Serial.begin( 115200 );
  Mouse.begin();
  //#if !defined(_MIPSEL_)
  //    while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
  //#endif
  Serial.println("Start");

  if (Usb.Init() == -1)
    Serial.println("OSC did not start.");

  delay( 200 );
  HidMouse.SetReportParser(0, &Prs);


}


using namespace std;

void loop()
{
  Usb.Task();
  if (Serial.available() > 0) {
    char d = Serial.read();
    Serial.println(d);

    //  * means the end of the data
    if (d == '*') {
      Serial.println(data);

      indexX = data.indexOf(',');
      indexY = data.indexOf(',', indexX + 1);
      indexState = data.indexOf(',', indexY + 1);
      indexAst = data.indexOf('*');
      x = data.substring(indexX + 1, indexY).toInt();
      y = data.substring(indexY + 1, indexState).toInt();
      state = data.substring(indexState + 1, indexAst - 1);

      Serial.print("X: ");
      Serial.println(x);
      Serial.print("Y: ");
      Serial.println(y);
      Serial.print("State: ");
      Serial.println(state);


      //        positive X
      if (x > 0) {
        while (x > 0) {
          Mouse.move(sensitivity, 0, 0);
          x -= 1;
          delay(aimDelay);
          aimDelay -= aimDeceleration;
        }
        //        negative X
      }
      else if (x < 0) {
        while (x < 0) {
          Mouse.move(-sensitivity, 0, 0);
          x += 1;
          delay(aimDelay);
          aimDelay -= aimDeceleration;
        }
      }

      //   positive Y
      if (y > 0) {
        while (y > 0) {
          Mouse.move(0, sensitivity, 0);
          y -= 1;
          delay(aimDelay);
          aimDelay -= aimDeceleration;
        }
      }
      //        negative Y
      else if (y < 0) {
        while (y < 0) {
          Mouse.move(0, -sensitivity, 0);
          y += 1;
          delay(aimDelay);
          aimDelay -= aimDeceleration;
        }
      }
      if (state == "shoot") {
        Mouse.click();
      }

      aimDelay = aimDelayDefault;
      data = "";
    } else {
      data += d;
    }
  }
}
