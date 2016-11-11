package com.hh.android.xampleapp;

import java.util.ArrayList;

/**
 * Author HieuHa on 011, 11 Nov 16.
 */

public interface HomeInterface {

    interface Presenter{
        void showObject1();
        void showList(ArrayList t);
    }

    interface View {
        void setPresenter(Presenter t);

        boolean isAdded();

        void showList(ArrayList t);
    }
}
