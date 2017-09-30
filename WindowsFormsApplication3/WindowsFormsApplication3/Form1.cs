using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using System.IO;

namespace WindowsFormsApplication3
{
    public partial class Form1 : Form
    {
        OpenFileDialog op = new OpenFileDialog();
        string file1="", file2="", file3="";
         StreamWriter wrr = new StreamWriter("../../input.txt", false);
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (op.ShowDialog() == DialogResult.OK)
            {
                textBox1.Text = op.FileName;
                file1 = op.FileName;

                wrr.WriteLine(file1);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (op.ShowDialog() == DialogResult.OK)
            {
                textBox2.Text = op.FileName;
                file2 = op.FileName;

            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (op.ShowDialog() == DialogResult.OK)
            {
                textBox3.Text = op.FileName;
                file3 = op.FileName;
                
            }

        }

        private void button5_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Select the original list you have, then select the regex command using the regex rules, then click on sort to get a new sorted file.","Help", MessageBoxButtons.OK);
        }

        private void button4_Click(object sender, EventArgs e)
        {

        }

        private void button4_Click_1(object sender, EventArgs e)
        {
            if (file1 != "" && file3 != "")
            {
                SaveFileDialog sv = new SaveFileDialog();
                sv.Filter = "CSV (*.csv)|*.csv";
                sv.DefaultExt = "csv";
                sv.AddExtension = true;
                sv.ShowDialog();
                textBox1.Text = sv.FileName;
                if (sv.FileName != "")
                {
                    int[] indexer = new int[8];
                    int i = 0;
                    string[,] files = new string[8, 3000];
                    Regex r;
                    StreamReader sr = new StreamReader(file1);
                    StreamReader sr2 = new StreamReader(file3);
                    StreamWriter wr = new StreamWriter(sv.FileName, false, Encoding.UTF8);
                    string CSVLine = "z", RegexLine = "z";
                    while (true)
                    {
                        RegexLine = sr2.ReadLine();
                        if (RegexLine == null)
                            break;
                        r = new Regex(RegexLine, RegexOptions.IgnoreCase);
                        while (true)
                        {
                            CSVLine = sr.ReadLine();
                            if (CSVLine == null)
                                break;
                            if (r.IsMatch(CSVLine))
                                files[i, indexer[i]++] = CSVLine;
                        }
                        i++;
                    }
                    for (i = 0; i < 8; i++)
                    {
                        for (int j = 0; j < indexer[i]; j++)
                        {
                            wr.WriteLine("Rank " + (8 - i).ToString() + " , " + files[i, j] + (80 - i * 10).ToString());
                        }
                    }
                    wr.Flush();
                    wrr.WriteLine(sv.FileName.ToString());
                    wrr.Flush();
                    wrr.Close();
                    wr.Close();
                    sr.Close();
                    sr2.Close();
                    Process p = new Process();
                    ProcessStartInfo startInfo = new ProcessStartInfo();
                    startInfo.WindowStyle = ProcessWindowStyle.Hidden;
                    startInfo.FileName = "cmd.exe";
                    startInfo.Arguments = "/c python " +"../../Sorting.py";
                    p.StartInfo = startInfo;
                    p.Start();
                    
                }
              
                
            }
            else
                MessageBox.Show("Please select the files first.", "ERROR", MessageBoxButtons.OK);
        }
    }
}
