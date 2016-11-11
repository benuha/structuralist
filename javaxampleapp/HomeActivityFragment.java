package com.hh.android.xampleapp;

import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.ArrayList;

/**
 * A placeholder fragment containing a simple view.
 */
public class HomeActivityFragment extends Fragment implements HomeInterface.View {

    private HomeInterface.Presenter mPresenter;

    public HomeActivityFragment() {
        // empty constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_main, container, false);
    }

    @Override
    public void setPresenter(HomeInterface.Presenter t) {
        this.mPresenter = t;
    }

    @Override
    public void showList(ArrayList t) {
        // update list view here
    }
}
