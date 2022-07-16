#include <TFile.h>
#include <TTree.h>

void create_input()
{
    TFile *fh=TFile::Open("input.root", "RECREATE");

    TTree *t = new TTree("Events", "");

    unsigned long br_unsignedlong = 0;
    t->Branch("br_unsignedlong", &br_unsignedlong);

    for(uint32_t i=0; i<=0xFFFFFF; i++) {
        br_unsignedlong = i;
        t->Fill();
    }
    t->Write();

    fh->Close();
}