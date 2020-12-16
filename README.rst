Text Classification
^^^^^^^^^^^^^^^^^^^

Vietnamese text classification problem is implemented in two ways: Naive Bayes classification algorithm and Neural network model.

Reference in https://nguyenvanhieu.vn/phan-loai-van-ban-tieng-viet and https://nguyenvanhieu.vn/xay-dung-mo-hinh-neural-network.

Dataset in https://github.com/duyvuleo/VNTC.

We got stopword.txt at https://xltiengviet.fandom.com/wiki/Danh_s%C3%A1ch_stop_word.


Installation Instruction
^^^^^^^^^^^^^^^^^^^^^^^^^

This tool requires Python 3 environment.

Direct your path to 'demo' directory by 'cd' command. To run this tool, you need to install numpy, regex, flask and pyvi module. Open your command prompt and run these commands:

.. code:: shell

    pip install numpy
    pip install regex
    pip install flask
    pip install pyvi
    python app.py

An IP address will appear in a few seconds (maybe it is http://127.0.0.1:5000). Type this address in a web browser and enter to use text classification tool.
