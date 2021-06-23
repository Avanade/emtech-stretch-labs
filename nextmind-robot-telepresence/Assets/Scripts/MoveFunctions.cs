using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class MoveFunctions : MonoBehaviour
{

    public DateTime time_start = DateTime.Now;
    public DateTime time_now = DateTime.Now;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    public async void on_start()
    {
        Debug.Log("an event has started");
        time_start = DateTime.Now;
        Debug.Log(time_start.ToString());
    }

    public async void open_grip()
    {
        Debug.Log("Open Grip Selected");
        Debug.Log("Read DateTime Public");
        Debug.Log(time_start.ToString());

        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);

        Debug.Log("Time Diff");
        Debug.Log(diffloat.ToString());


        StartCoroutine(Upload("opengrip", diffloat * 10));
    }

    public void close_grip()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        Debug.Log("Close Grip Selected");
        StartCoroutine(Upload("closegrip", diffloat * 10));
    }

    public void arm_up()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        StartCoroutine(Upload("armup", diffloat / 10));
    }
    public void arm_down()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        StartCoroutine(Upload("armdown", diffloat / 10));
    }
    public void arm_in()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        StartCoroutine(Upload("armin", diffloat / 10));
    }
    public void arm_out()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        StartCoroutine(Upload("armout", diffloat / 10));
    }
    public void forward()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        StartCoroutine(Upload("forwards", diffloat / 10));
    }
    public void backwards()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        StartCoroutine(Upload("backwards", diffloat / 10));
    }
    public void left()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        StartCoroutine(Upload("left", diffloat / 10));
    }
    public void right()
    {
        time_now = DateTime.Now;
        System.TimeSpan diff = time_now.Subtract(time_start);
        float diffloat = Convert.ToSingle(diff.TotalSeconds);
        StartCoroutine(Upload("right", diffloat / 10));
    }

    IEnumerator Upload(string method, float ammount)
    {
        WWWForm form = new WWWForm();
        form.AddField("myField", "myData");
        Debug.Log("Attempting Network Request");
        using (UnityWebRequest www = UnityWebRequest.Post($"[server.path.here]/{method}/{ammount}", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                Debug.Log("Form upload complete!");
            }
        }
    }
}
