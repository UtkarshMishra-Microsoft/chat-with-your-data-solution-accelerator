import { Outlet, Link } from "react-router-dom";
import styles from "./Layout.module.css";
// import Azure from "../../assets/Azure.svg";
import {
  CopyRegular,
  ShareRegular,
  ShareAndroid16Filled,
  NoteAdd16Filled,
  ArrowBidirectionalUpDown16Filled
} from "@fluentui/react-icons";
import { Dialog, Stack, TextField } from "@fluentui/react";
import { Tooltip } from "@fluentui/react-components";
import { useEffect, useState } from "react";

const Layout = () => {
    const [isSharePanelOpen, setIsSharePanelOpen] = useState<boolean>(false);
    const [copyClicked, setCopyClicked] = useState<boolean>(false);
    const [copyText, setCopyText] = useState<string>("Copy URL");

    const handleShareClick = () => {
        setIsSharePanelOpen(true);
    };

    const handleSharePanelDismiss = () => {
        setIsSharePanelOpen(false);
        setCopyClicked(false);
        setCopyText("Copy URL");
    };

    const handleCopyClick = () => {
        navigator.clipboard.writeText(window.location.href);
        setCopyClicked(true);
    };

    const resetCopyClick = () => {
      setTimeout(() => {
        setCopyClicked(false);
      }, 500);
    };

    useEffect(() => {
        if (copyClicked) {
            setCopyText("Copied URL");
        }
    }, [copyClicked]);

    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <Stack horizontal verticalAlign="center">

                        <Link to="/" className={styles.headerTitleContainer}>
                            <img
                            src="../../src/assets/logo.svg"
                            className={styles.headerIcon}
                            aria-hidden="true"
                            />
                            <h3 className={styles.headerTitle}>Pronto</h3>
                        </Link>

                        <div className={styles.mainNavLinks}>
                          <Tooltip content={{ children:
                            // ↓ this is where you form the tooltip content
                            <div className={styles.dataSourceToolTipInner}>
                              <span>Add a data source</span>
                            </div>,
                            className: styles.dataSourceToolTip
                          }} relationship="label" positioning={'below'}>
                            {/* ↓ this is where the hoverable content goes */}
                            <div className={styles.addSourceButtonContainer}>
                              <a href="https://rsta4xey-test-website-6eg6fe2yksguu-admin.azurewebsites.net/Ingest_Data" target="_blank" rel="noopener noreferrer">
                                {/* <NoteAdd16Filled className={styles.addSourceButton} /> */}
                                <img
                                  src="../../addSourceIcon.png"
                                  className={styles.addSourceButton}
                                  aria-hidden="true"
                                  />
                              </a>
                            </div>
                          </Tooltip>


                          <Tooltip content={{ children:
                            // ↓ this is where you form the tooltip content
                            <div className={styles.shareToolTipInner}>
                              {!copyClicked ? (
                                <span>Share Pronto</span>
                              ) : (
                                <div className={styles.copiedToClipboard}>
                                  <img src="../../copiedIcon.png" alt="Pronto link copied to clipbaord" />
                                  <span>Link copied to clipboard!</span>
                                </div>
                              )}
                            </div>,
                            className: styles.shareToolTip
                          }} relationship="label" positioning={'below'}>
                            {/* ↓ this is where the hoverable content goes */}
                            <div className={styles.shareButtonContainer} role="button" tabIndex={0} aria-label="Share" onClick={handleCopyClick} onKeyDown={e => e.key === "Enter" || e.key === " " ? handleCopyClick() : null} onMouseLeave={e => resetCopyClick()}>
                              {/* <ShareAndroid16Filled className={styles.shareButton} /> */}
                              <img
                                src="../../shareLinkIcon.png"
                                className={styles.shareButton}
                                aria-hidden="true"
                                />
                            </div>
                          </Tooltip>


                          <div className={`${styles.userMenuContainer} ${styles.disabled}`}>
                            <div className={styles.userMenuBtn}>
                              <span>Eddie Hoover</span>
                              <div className={styles.userMenuArrows}>{'<  >'}</div>
                            </div>
                            {/* <div>Future menu content</div> */}
                          </div>

                        </div>

                    </Stack>
                </div>
            </header>
            <Outlet />
            <Dialog
                onDismiss={handleSharePanelDismiss}
                hidden={!isSharePanelOpen}
                styles={{

                    main: [{
                        selectors: {
                          ['@media (min-width: 480px)']: {
                            maxWidth: '600px',
                            background: "#FFFFFF",
                            boxShadow: "0px 14px 28.8px rgba(0, 0, 0, 0.24), 0px 0px 8px rgba(0, 0, 0, 0.2)",
                            borderRadius: "8px",
                            maxHeight: '200px',
                            minHeight: '100px',
                          }
                        }
                      }]
                }}
                dialogContentProps={{
                    title: "Share this Pronto thread!",
                    showCloseButton: true
                }}
            >
                <Stack horizontal verticalAlign="center" style={{gap: "8px"}}>
                    <TextField className={styles.urlTextBox} defaultValue={window.location.href} readOnly/>
                    <div
                        className={styles.copyButtonContainer}
                        role="button"
                        tabIndex={0}
                        aria-label="Copy"
                        onClick={handleCopyClick}
                        onKeyDown={e => e.key === "Enter" || e.key === " " ? handleCopyClick() : null}
                    >
                        <CopyRegular className={styles.copyButton} />
                        <span className={styles.copyButtonText}>{copyText}</span>
                    </div>
                </Stack>
            </Dialog>
        </div>
    );
};

export default Layout;
