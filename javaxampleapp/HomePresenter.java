package com.hh.android.xampleapp;

import android.content.Context;

import java.util.ArrayList;

/**
 * Author HieuHa on 011, 11 Nov 16.
 */

public class HomePresenter implements HomeInterface.Presenter {

    private Context mContext;
    private HomeInterface.View mView;
    public HomePresenter(Context context, HomeInterface.View v){
        this.mContext = context;
        this.mView = v;
        mView.setPresenter(this);
    }

    @Override
    public void showObject1() {
        // nothing here
    }

    @Override
    public void showList(ArrayList t) {
        if (mView.isAdded())
            mView.showList(t);
    }
}
